"""Build the control panel manufacturing manual (PDF) from the chapter sources in src/.

    .venv\\Scripts\\python.exe docs\\control_panel_manual\\build.py

Writes the full manual and upload-sized parts to Desktop/Control_Panel_Manual/. Chapters are grouped into parts so
that each part stays under the app's ingestion limit (MAX_FILE_CHUNKS = 400), counted with the
app's own extractor and splitter. Run figures.py first when a diagram changes; --no-parts builds
only the full manual. Appendix A (alarm codes) is regenerated from the machine chapters.
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = HERE / "src"
FIGS = HERE / "figures"
OUT = Path.home() / "Desktop" / "Control_Panel_Manual"

DOC_NO = "CPM-MAN-001"
TITLE = "Control Panel Manufacturing: Plant, Machines and Technician Manual"
SHORT = "CPM-MAN-001 Control Panel Manufacturing Manual (SAMPLE)"
PAGE = pymupdf.paper_rect("a4")
BODY = pymupdf.Rect(56, 62, PAGE.width - 56, PAGE.height - 58)

CSS = """
body { font-family: sans-serif; font-size: 10pt; line-height: 1.4; color: #1d1d1d; }
h1 { font-size: 19pt; color: #0b3d6e; margin: 0 0 8pt 0; padding-bottom: 4pt;
     border-bottom: 2px solid #0b3d6e; page-break-before: always; }
h2 { font-size: 13.5pt; color: #0b3d6e; margin: 14pt 0 4pt 0; }
h3 { font-size: 11pt; color: #24507f; margin: 10pt 0 3pt 0; }
p { margin: 0 0 6pt 0; text-align: justify; }
ul, ol { margin: 0 0 6pt 0; padding-left: 16pt; }
li { margin: 0 0 2pt 0; }
table { border-collapse: collapse; margin: 4pt 0 9pt 0; width: 100%; }
th { color: #0b3d6e; border: 0.7px solid #6b7c93; padding: 2.5pt 4pt; font-size: 9pt;
     text-align: left; }
td { border: 0.7px solid #9aa7b8; padding: 2.5pt 4pt; font-size: 9pt; vertical-align: top; }
.box { padding: 0; margin: 4pt 0 9pt 0; }
.box p { margin: 4pt 7pt 4pt 7pt; text-align: left; }
.box ul, .box ol { margin: 0 7pt 4pt 7pt; }
.danger  { background-color: #fde7e7; border: 1.2px solid #b3261e; }
.warning { background-color: #fff3d6; border: 1.2px solid #c77700; }
.caution { background-color: #fff8e5; border: 1px solid #c79a00; }
.note    { background-color: #eaf2fb; border: 1px solid #4a78a8; }
.tip     { background-color: #e9f6ec; border: 1px solid #2f7d46; }
.hinglish{ background-color: #f2ecfa; border: 1px solid #6a4c9c; }
.fig { text-align: center; margin: 6pt 0 10pt 0; }
.cap { font-size: 8.5pt; color: #444; text-align: center; }
.toc1 { font-weight: bold; margin: 5pt 0 0 0; }
.toc2 { margin: 0 0 0 14pt; font-size: 9.5pt; }
.cover { text-align: center; }
"""

BOX_KINDS = {
    "DANGER": "danger", "WARNING": "warning", "CAUTION": "caution",
    "NOTE": "note", "TIP": "tip", "HINGLISH": "hinglish",
}
BOX_LABEL = {"HINGLISH": "Operator ke liye (Hinglish)"}


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", out)
    # An invisible soft hyphen after "f" stops the font from forming fi / ff / fl ligatures, which
    # PDF text extraction returns as single characters: a search for "filter" would miss them.
    return re.sub(r"f(?=[fil])", "f­", out)


def list_html(lines: list[str]) -> str:
    ordered = re.match(r"\d+[.)] ", lines[0]) is not None
    items, current = [], None
    for ln in lines:
        m = re.match(r"(?:- |\d+[.)] )(.*)", ln)
        if m:
            current = [m.group(1)]
            items.append(current)
        elif current is not None:
            current.append(ln.strip())
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(f"<li>{inline(' '.join(i))}</li>" for i in items) + f"</{tag}>"


def table_html(lines: list[str]) -> str:
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
    head, body = rows[0], rows[1:]
    out = ["<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>"]
    for r in body:
        r = r + [""] * (len(head) - len(r))
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    return "".join(out) + "</table>"


def block_html(block: list[str]) -> str:
    first = block[0]
    if first.startswith("### "):
        return f"<h3>{inline(first[4:])}</h3>" + (block_html(block[1:]) if block[1:] else "")
    if first.startswith("## "):
        return f"<h2>{inline(first[3:])}</h2>" + (block_html(block[1:]) if block[1:] else "")
    if first.startswith("# "):
        return f"<h1>{inline(first[2:])}</h1>" + (block_html(block[1:]) if block[1:] else "")
    if first.startswith("[[fig:"):
        m = re.match(r"\[\[fig:([\w.-]+)\|(.+?)(?:\|(\d+))?\]\]", first)
        name, cap, width = m.group(1), m.group(2), m.group(3) or "440"
        return (f'<div class="fig"><img src="{name}.png" width="{width}"/>'
                f'<p class="cap">{inline(cap)}</p></div>')
    m = re.match(r"!! (\w+): ?(.*)", first)
    if m and m.group(1) in BOX_KINDS:
        kind = m.group(1)
        label = BOX_LABEL.get(kind, kind)
        rest = [m.group(2)] + block[1:] if m.group(2) else block[1:]
        inner, para = [], []
        i = 0
        while i < len(rest):
            if re.match(r"(- |\d+[.)] )", rest[i]):
                j = i
                while j < len(rest) and (re.match(r"(- |\d+[.)] )", rest[j]) or rest[j].startswith("  ")):
                    j += 1
                if para:
                    inner.append(f"<p>{inline(' '.join(para))}</p>")
                    para = []
                inner.append(list_html(rest[i:j]))
                i = j
            else:
                para.append(rest[i])
                i += 1
        if para:
            inner.append(f"<p>{inline(' '.join(para))}</p>")
        inner[0] = inner[0].replace("<p>", f"<p><b>{label}:</b> ", 1) if inner[0].startswith("<p>") \
            else f"<p><b>{label}:</b></p>" + inner[0]
        return f'<div class="box {BOX_KINDS[kind]}">' + "".join(inner) + "</div>"
    if first.lstrip().startswith("|"):
        return table_html(block)
    if re.match(r"(- |\d+[.)] )", first):
        return list_html(block)
    return f"<p>{inline(' '.join(block))}</p>"


def md_to_html(text: str) -> str:
    out, block = [], []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            if block:
                out.append(block_html(block))
                block = []
            continue
        # A heading always starts its own block
        if line.startswith("#") and block:
            out.append(block_html(block))
            block = []
        block.append(line)
        if line.startswith("#"):
            out.append(block_html(block))
            block = []
    if block:
        out.append(block_html(block))
    return "\n".join(out)


def chapters() -> list[Path]:
    return sorted(SRC.glob("*.md"))


CODE_ASSET = {
    "SH": "SHEAR-01", "TP": "PUNCH-02", "LS": "LASER-03", "PB": "BRAKE-04", "SW": "WELD-05",
    "MG": "WELD-06", "PM": "PEM-07", "PT": "PTL-08", "PC": "PCL-09", "BB": "BUS-10", "WR": "WIRE-11",
    "CR": "CRIMP-12", "MK": "MARK-13", "CP": "COMP-15",
}
FAULT_APPENDIX = "50_appendix_a_fault_codes.md"


def write_fault_code_appendix() -> None:
    """Appendix A: every alarm code of the machine chapters in one list, taken from those chapters' tables."""
    rows = []
    for f in chapters():
        if f.name == FAULT_APPENDIX:
            continue
        header = None
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                header = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells[0] == "Code":
                header = cells
                continue
            if header and re.fullmatch(r"[A-Z]{2}-\d{2}", cells[0]):
                rec = dict(zip(header, cells))
                cause = rec.get("Cause", "")
                action = rec.get("Action", "")
                rows.append((cells[0], rec.get("Message", ""), cause, action))
    # Alarms written inline in a symptom table (e.g. CP-01 in the compressor chapter)
    for f in chapters():
        if f.name == FAULT_APPENDIX:
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\| ([A-Z]{2}-\d{2}) ([^|]+)\| ([^|]+)\| ([^|]+)\|", line)
            if m and m.group(1)[:2] in CODE_ASSET and m.group(1) not in {r[0] for r in rows}:
                rows.append((m.group(1), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()))
    order = list(CODE_ASSET)
    rows.sort(key=lambda r: (order.index(r[0][:2]), r[0]))
    out = ["# Appendix A. Alarm and Fault Code Master List", "",
           "This appendix collects every alarm code used in the machine chapters, sorted by machine. The "
           "machine chapter gives the full troubleshooting table; this list is for quick look-up when an "
           "alarm appears on a screen. The codes are the plant's own codes for the demonstration factory "
           "(see the note at the start of the manual).", ""]
    current = None
    for code, msg, cause, action in rows:
        prefix = code[:2]
        if prefix != current:
            current = prefix
            out += ["", f"## Codes {prefix}-xx: {CODE_ASSET[prefix]}", "",
                    "| Code | Machine | Message | Cause | Action |", "|---|---|---|---|---|"]
        out.append(f"| {code} | {CODE_ASSET[prefix]} | {msg} | {cause or '-'} | {action} |")
    out += ["", "!! NOTE: An alarm that comes back after reset is a symptom, not the fault. Record every "
            "repeated alarm in the breakdown record with the asset code and the code shown (for example "
            "\"BRAKE-04, PB-12\"), so that repeated causes can be found in the history.", ""]
    (SRC / FAULT_APPENDIX).write_text("\n".join(out), encoding="utf-8")


def cover_html() -> str:
    return f"""
<div class="cover">
<p style="font-size:11pt;color:#555;margin-top:120pt">{DOC_NO} &#183; Revision A &#183; SAMPLE DOCUMENT</p>
<p style="font-size:26pt;color:#0b3d6e;font-weight:bold;line-height:1.2;margin-top:18pt">
Control Panel Manufacturing</p>
<p style="font-size:16pt;color:#24507f;margin-top:4pt">Plant Process, Machine Working, Operator Instructions
and Technician Guidance</p>
<p style="font-size:11pt;margin-top:40pt">For operators, technicians, supervisors and maintenance staff of an
electrical control panel (LT switchboard, MCC, PCC, APFC and PLC panel) factory.</p>
<p style="font-size:10pt;color:#8a1c1c;margin-top:60pt">This manual is a sample document prepared for the
ContextBasedRAG demonstration factory. The factory, the machines, their codes and every value in it are
invented, written from common industry practice. It must not be used to operate or repair a real machine:
always follow the manufacturer's manual and the site's own approved procedures.</p>
</div>
"""


def toc_html(positions) -> str:
    rows = []
    for p in positions:
        if p.heading not in (1, 2) or p.open_close != 1 or not p.id:
            continue
        cls = "toc1" if p.heading == 1 else "toc2"
        text = re.sub(r"f(?=[fil])", "f­", html.escape(p.text.replace("­", "")))
        rows.append(f'<p class="{cls}"><a href="#{p.id}">{text}</a>'
                    f' &#183; page {p.page_num}</p>')
    return "<h1>Contents</h1>" + "\n".join(rows)


def build(md_files: list[Path], out_path: Path, part_label: str | None = None) -> pymupdf.Document:
    body = "\n".join(md_to_html(f.read_text(encoding="utf-8")) for f in md_files)
    archive = pymupdf.Archive(str(FIGS)) if FIGS.is_dir() else None
    cover = cover_html()
    if part_label:
        cover = cover.replace("SAMPLE DOCUMENT", f"SAMPLE DOCUMENT &#183; {part_label}")
    cover = re.sub(r"f(?=[fil])", "f­", cover)

    def contentfn(positions):
        return cover + toc_html(positions) + body

    def rectfn(rect_num, filled):
        return PAGE, BODY, None

    doc = pymupdf.Story.write_stabilized_with_links(
        contentfn, rectfn, user_css=CSS, archive=archive, add_header_ids=True
    )
    # Running header and footer (kept short: they are part of every page's extracted text)
    n = doc.page_count
    for i, page in enumerate(doc):
        if i == 0:
            continue
        page.draw_line((56, 50), (PAGE.width - 56, 50), color=(0.04, 0.24, 0.43), width=0.6)
        page.insert_text((56, 45), SHORT + (f" - {part_label}" if part_label else ""),
                         fontsize=7.5, color=(0.3, 0.3, 0.3))
        page.insert_text((PAGE.width - 110, PAGE.height - 34), f"Page {i + 1} of {n}",
                         fontsize=8, color=(0.3, 0.3, 0.3))
    doc.set_metadata({"title": TITLE + (f" ({part_label})" if part_label else ""),
                      "author": "ContextBasedRAG sample data", "subject": "Control panel manufacturing",
                      "keywords": "control panel, MCC, PCC, sheet metal, busbar, wiring, testing, maintenance"})
    doc.save(out_path, garbage=4, deflate=True)
    return doc


def add_outline(doc_path: Path) -> None:
    """PDF bookmarks from the chapter and section headings found on the pages."""
    doc = pymupdf.open(doc_path)
    toc = []
    for pno, page in enumerate(doc, start=1):
        if pno <= 1:
            continue
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                spans = line["spans"]
                if not spans:
                    continue
                size = spans[0]["size"]
                text = "".join(s["text"] for s in spans).strip()
                if size > 18.5 and text and text != "Contents":
                    if toc and toc[-1][0] == 1 and toc[-1][2] == pno:
                        toc[-1][1] += " " + text  # chapter title wrapped onto a second line
                    else:
                        toc.append([1, text, pno])
                elif 13 < size < 14 and text and toc:
                    toc.append([2, text, pno])
    doc.set_toc(toc)
    doc.saveIncr()


def _splitter():
    sys.path.insert(0, str(ROOT))
    from backend.app.services import ingestion  # noqa: E402
    return ingestion


def chunk_count(pdf_path: Path) -> int:
    ingestion = _splitter()
    return len(ingestion.split(ingestion.extract(pdf_path, "pdf")))


def chapter_title(f: Path) -> str:
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


CHUNK_BUDGET = 340  # per part, below MAX_FILE_CHUNKS = 400 with room for cover and contents


def plan_parts(full: Path, files: list[Path]) -> list[list[Path]]:
    """Group chapters (in order) into parts whose chunk count stays under CHUNK_BUDGET."""
    ingestion = _splitter()
    pages = ingestion.extract(full, "pdf")
    per_page = [len(ingestion.split([pg])) for pg in pages]
    toc = [t for t in pymupdf.open(full).get_toc() if t[0] == 1]
    starts, i = [], 0
    for f in files:
        title = chapter_title(f)
        if not title:  # continuation file (no chapter heading): belongs to the previous chapter
            starts.append(None)
            continue
        while i < len(toc) and not title.startswith(unicodedata.normalize("NFKC", toc[i][1])[:40]):
            i += 1
        if i == len(toc):
            raise SystemExit(f"Chapter not found in outline: {title}")
        starts.append(toc[i][2])
        i += 1
    # page range of each file; continuation files count with the chapter before them
    groups, cur = [], []
    for f, st in zip(files, starts):
        if st is None and cur:
            cur[-1][0].append(f)
        else:
            cur.append(([f], st))
    bounds = [st for _, st in cur] + [len(per_page) + 1]
    chunks = [sum(per_page[bounds[k] - 1:bounds[k + 1] - 1]) for k in range(len(cur))]
    parts, part, total = [], [], 0
    for (fs, _), c in zip(cur, chunks):
        if part and total + c > CHUNK_BUDGET:
            parts.append(part)
            part, total = [], 0
        part += fs
        total += c
    if part:
        parts.append(part)
    return parts


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write_fault_code_appendix()
    files = chapters()
    full = OUT / "CPM-MAN-001_control_panel_manufacturing_manual_FULL.pdf"
    build(files, full)
    add_outline(full)
    d = pymupdf.open(full)
    print(f"{full.name}: {d.page_count} pages, {full.stat().st_size / 1e6:.2f} MB, {chunk_count(full)} chunks")
    d.close()
    if "--no-parts" in sys.argv:
        return
    for old in OUT.glob("CPM-MAN-001_Part*.pdf"):
        old.unlink()
    parts = plan_parts(full, files)
    for k, chosen in enumerate(parts, start=1):
        first, last = chapter_title(chosen[0]), chapter_title(chosen[-1]) or chapter_title(chosen[-2])
        label = f"Part {k} of {len(parts)}"
        out = OUT / f"CPM-MAN-001_Part{k}_of_{len(parts)}.pdf"
        build(chosen, out, label)
        add_outline(out)
        d = pymupdf.open(out)
        n = chunk_count(out)
        print(f"{out.name}: {d.page_count} pages, {out.stat().st_size / 1e6:.2f} MB, {n} chunks "
              f"({first} ... {last})")
        d.close()
        if n > 400:
            raise SystemExit(f"{out.name} has {n} chunks, above the app limit of 400")


if __name__ == "__main__":
    main()
