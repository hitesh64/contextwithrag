"""Draw the manual's diagrams as PNG files in figures/ (run before build.py)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "figures"
FONT = "C:/Windows/Fonts/arial.ttf"
BOLD = "C:/Windows/Fonts/arialbd.ttf"
S = 2  # supersampling: draw at 2x, the PDF scales it down

NAVY = (11, 61, 110)
BLUE = (223, 232, 243)
GREY = (90, 90, 90)
LIGHT = (245, 245, 245)
RED = (179, 38, 30)
PINK = (253, 231, 231)
GREEN = (47, 125, 70)
LGREEN = (233, 246, 236)
ORANGE = (199, 119, 0)
LORANGE = (255, 243, 214)
COPPER = (196, 112, 54)
STEEL = (170, 178, 189)


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size * S)


class Fig:
    def __init__(self, w, h):
        self.im = Image.new("RGB", (w * S, h * S), "white")
        self.d = ImageDraw.Draw(self.im)

    def box(self, x, y, w, h, text, fill=BLUE, outline=NAVY, size=12, bold=False, radius=6, color=(20, 20, 20)):
        self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], radius * S, fill=fill,
                                 outline=outline, width=2 * S // 2 + 1)
        self.text_c(x + w / 2, y + h / 2, text, size, bold, color)

    def rect(self, x, y, w, h, fill=LIGHT, outline=GREY, width=1):
        self.d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], fill=fill, outline=outline, width=width * S)

    def text_c(self, cx, cy, text, size=12, bold=False, color=(20, 20, 20)):
        f = font(size, bold)
        lines = text.split("\n")
        hs = [self.d.textbbox((0, 0), ln, font=f)[3] for ln in lines]
        total = sum(hs) + (len(lines) - 1) * 3 * S
        y = cy * S - total / 2
        for ln, h in zip(lines, hs):
            w = self.d.textlength(ln, font=f)
            self.d.text((cx * S - w / 2, y), ln, font=f, fill=color)
            y += h + 3 * S

    def text(self, x, y, text, size=11, bold=False, color=(20, 20, 20)):
        self.d.text((x * S, y * S), text, font=font(size, bold), fill=color)

    def line(self, pts, color=GREY, width=2):
        self.d.line([(x * S, y * S) for x, y in pts], fill=color, width=width * S)

    def arrow(self, x1, y1, x2, y2, color=NAVY, width=2):
        self.line([(x1, y1), (x2, y2)], color, width)
        import math
        a = math.atan2(y2 - y1, x2 - x1)
        L = 8
        p1 = (x2 - L * math.cos(a - 0.45), y2 - L * math.sin(a - 0.45))
        p2 = (x2 - L * math.cos(a + 0.45), y2 - L * math.sin(a + 0.45))
        self.d.polygon([(x2 * S, y2 * S), (p1[0] * S, p1[1] * S), (p2[0] * S, p2[1] * S)], fill=color)

    def circle(self, cx, cy, r, fill=BLUE, outline=NAVY):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill, outline=outline,
                       width=2 * S)

    def poly(self, pts, fill=STEEL, outline=GREY):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)

    def save(self, name):
        OUT.mkdir(exist_ok=True)
        self.im.save(OUT / f"{name}.png", optimize=True)


def chain(f, items, x0, y, w, h, gap, size=11, fill=BLUE):
    """Boxes in a row joined by arrows."""
    for i, t in enumerate(items):
        x = x0 + i * (w + gap)
        f.box(x, y, w, h, t, fill=fill, size=size)
        if i:
            f.arrow(x - gap + 2, y + h / 2, x - 2, y + h / 2)


def plant_flow():
    f = Fig(760, 330)
    row1 = ["Raw material\nstore", "Cutting\nLASER-03\nPUNCH-02\nSHEAR-01", "Bending\nBRAKE-04",
            "Welding and\nhardware\nWELD-05/06\nPEM-07", "Pre-treatment\nPTL-08"]
    chain(f, row1, 10, 30, 128, 80, 24)
    row2 = ["Dispatch", "Packing", "Testing\nTEST-14", "Wiring", "Assembly", "Powder coating\nPCL-09"]
    for i, t in enumerate(row2):
        x = 10 + i * 124
        f.box(x, 200, 104, 70, t, fill=LGREEN if i < 3 else BLUE, outline=GREEN if i < 3 else NAVY)
        if i:
            f.arrow(x - 2, 235, x - 20 + 2, 235)
    f.arrow(10 + 4 * 152 + 64, 112, 10 + 5 * 124 + 52, 198)
    f.box(380, 128, 170, 52, "Busbar BUS-10\nWire prep WIRE-11/12/13", fill=LORANGE, outline=ORANGE, size=10)
    f.arrow(440, 182, 10 + 4 * 124 + 52, 198, color=ORANGE)
    f.text(10, 6, "Bays 1-3: fabrication and paint", 11, True, NAVY)
    f.text(10, 290, "Bays 4-6: busbar, wiring, assembly, testing, packing", 11, True, GREEN)
    f.save("plant_flow")


def loto_steps():
    f = Fig(760, 250)
    steps = ["1 Prepare", "2 Inform", "3 Shut\ndown", "4 Isolate", "5 Lock\nand tag", "6 Release\nstored energy",
             "7 Verify\nzero energy", "8 Work, then\nremove LOTO"]
    for i, t in enumerate(steps):
        row, col = divmod(i, 4)
        x = 20 + col * 185
        y = 30 + row * 110
        fill = PINK if i in (4, 6) else BLUE
        f.box(x, y, 150, 70, t, fill=fill, outline=RED if i in (4, 6) else NAVY, size=13, bold=True)
        if col:
            f.arrow(x - 33, y + 35, x - 2, y + 35)
    f.line([(20 + 3 * 185 + 75, 102), (20 + 3 * 185 + 75, 120), (95, 120), (95, 138)], NAVY, 2)
    f.arrow(95, 128, 95, 138)
    f.text(20, 225, "Red steps: never skip. Your own lock on every isolation point; test-test-test before touch.",
           11, True, RED)
    f.save("loto_steps")


def label(f, x, y, tx, ty, text, size=10):
    """Leader line from a point on the drawing to a text label."""
    f.line([(x, y), (tx, ty)], GREY, 1)
    f.circle(x, y, 2.5, fill=GREY, outline=GREY)
    w = f.d.textlength(text, font=font(size)) / S
    f.text(tx + 4 if tx >= x else max(2, tx - 4 - w), ty - size * 0.6, text, size)


def fig_shear():
    f = Fig(640, 340)
    f.rect(140, 230, 340, 40, fill=STEEL)  # table
    f.rect(330, 214, 30, 16, fill=(110, 110, 120))  # lower blade
    f.poly([(300, 40), (380, 40), (380, 170), (362, 196), (340, 196), (340, 170), (300, 170)], fill=STEEL)
    f.rect(340, 176, 22, 22, fill=(110, 110, 120))  # upper blade
    f.rect(272, 150, 18, 64, fill=(120, 150, 190))  # hold down
    f.rect(240, 200, 30, 6, fill=(230, 200, 60), outline=GREY)  # finger guard
    f.rect(100, 214, 420, 4, fill=(60, 60, 60), outline=(60, 60, 60))  # sheet
    f.rect(500, 186, 10, 30, fill=ORANGE)  # back gauge finger
    f.line([(510, 200), (600, 200)], GREY, 3)
    f.rect(320, 0, 40, 40, fill=(200, 210, 225))
    f.arrow(395, 70, 395, 150, RED, 3)
    label(f, 310, 100, 420, 22, "Blade holder (beam) moved by hydraulic cylinders")
    label(f, 351, 190, 420, 110, "Upper blade")
    label(f, 345, 222, 420, 300, "Lower blade on table")
    label(f, 280, 160, 160, 120, "Hold-down")
    label(f, 255, 203, 120, 170, "Finger guard")
    label(f, 150, 216, 40, 300, "Sheet")
    label(f, 505, 190, 540, 150, "Back gauge")
    f.text(20, 318, "Rake angle: upper blade inclined 0.5 to 2.5 degrees along its length; blade gap set by thickness.", 10,
           False, NAVY)
    f.save("shear")


def fig_turret():
    f = Fig(640, 360)
    f.rect(20, 120, 600, 220, fill=(248, 248, 248))  # table
    f.rect(120, 150, 300, 160, fill=(225, 230, 236))  # sheet
    for i, x in enumerate((150, 260, 370)):
        f.rect(x, 300, 26, 22, fill=ORANGE)  # clamps
    f.rect(100, 318, 360, 12, fill=STEEL)  # carriage
    f.circle(470, 120, 95, fill=(232, 238, 246))
    f.circle(470, 120, 60, fill=(245, 248, 252))
    import math
    for k in range(16):
        a = k * 2 * math.pi / 16
        f.circle(470 + 78 * math.cos(a), 120 + 78 * math.sin(a), 8 if k % 4 else 12, fill=STEEL)
    f.circle(470, 198, 13, fill=PINK, outline=RED)
    f.arrow(250, 345, 400, 345, NAVY)
    f.text(405, 336, "X", 12, True, NAVY)
    f.arrow(90, 300, 90, 170, NAVY)
    f.text(76, 150, "Y", 12, True, NAVY)
    label(f, 470, 198, 560, 260, "Ram / punching point")
    label(f, 545, 80, 575, 30, "Turret stations")
    label(f, 163, 310, 40, 285, "Clamps")
    label(f, 250, 230, 200, 100, "Sheet moved under the ram")
    label(f, 300, 324, 300, 352, "Carriage", 9)
    f.save("turret")


def fig_laser():
    f = Fig(700, 280)
    f.box(10, 100, 120, 60, "Fiber laser\nsource 3 kW", fill=PINK, outline=RED)
    f.line([(130, 130), (200, 130), (230, 60), (300, 60)], ORANGE, 4)
    f.text(160, 70, "Delivery fibre", 10)
    f.box(300, 30, 110, 210, "", fill=BLUE)
    for i, (t, y) in enumerate([("Collimator", 50), ("Focus lens", 100), ("Protective window", 145)]):
        f.rect(310, y, 90, 10, fill=(200, 230, 255), outline=NAVY)
        f.text(420, y - 3, t, 10)
    f.poly([(325, 200), (385, 200), (365, 236), (345, 236)], fill=STEEL)
    f.text(420, 205, "Nozzle + height sensor", 10)
    f.line([(355, 160), (355, 240)], RED, 2)
    f.rect(260, 244, 200, 8, fill=(80, 80, 80))
    f.text(470, 240, "Sheet (0.5-1 mm below nozzle)", 10)
    f.box(560, 20, 130, 48, "Assist gas\nO2 / N2 / air", fill=LGREEN, outline=GREEN, size=10)
    f.arrow(560, 44, 412, 190, GREEN)
    f.box(560, 110, 130, 48, "Chiller\n25 / 28 deg C", fill=BLUE, size=10)
    f.arrow(560, 134, 412, 120, NAVY)
    f.arrow(560, 140, 132, 140, NAVY)
    f.box(560, 200, 130, 48, "Fume extractor", fill=LORANGE, outline=ORANGE, size=10)
    f.save("laser")


def fig_press_brake():
    f = Fig(680, 330)
    # punch
    f.poly([(150, 30), (230, 30), (230, 120), (195, 175), (185, 175), (150, 120)], fill=STEEL)
    # die
    f.poly([(110, 230), (270, 230), (270, 290), (110, 290)], fill=STEEL)
    f.poly([(160, 230), (220, 230), (190, 262)], fill="white")
    # sheet bent
    f.line([(60, 205), (185, 178), (190, 180), (195, 178), (320, 205)], (40, 40, 40), 4)
    f.arrow(250, 60, 250, 140, RED, 3)
    label(f, 190, 80, 270, 25, "Punch (upper tool)")
    label(f, 250, 270, 290, 285, "V-die (lower tool)")
    f.line([(160, 300), (220, 300)], NAVY, 1)
    f.text(172, 302, "V = 8 t", 10, True, NAVY)
    label(f, 300, 202, 330, 240, "Sheet touches punch tip and die shoulders only")
    # axes schematic
    x0 = 420
    f.rect(x0, 40, 230, 30, fill=BLUE, outline=NAVY)
    f.text(x0 + 70, 46, "Ram (upper beam)", 11, True, NAVY)
    f.arrow(x0 + 15, 75, x0 + 15, 120, RED, 2)
    f.text(x0 + 2, 122, "Y1", 11, True, RED)
    f.arrow(x0 + 215, 75, x0 + 215, 120, RED, 2)
    f.text(x0 + 205, 122, "Y2", 11, True, RED)
    f.rect(x0, 160, 230, 26, fill=STEEL)
    f.text(x0 + 50, 165, "Table with crowning (V axis)", 10)
    f.rect(x0 + 90, 200, 12, 40, fill=ORANGE)
    f.arrow(x0 + 108, 220, x0 + 180, 220, NAVY)
    f.text(x0 + 185, 212, "X", 11, True, NAVY)
    f.arrow(x0 + 96, 250, x0 + 96, 285, NAVY)
    f.text(x0 + 102, 270, "R", 11, True, NAVY)
    f.arrow(x0 + 60, 300, x0 + 140, 300, NAVY)
    f.text(x0 + 145, 293, "Z1/Z2", 11, True, NAVY)
    f.text(x0, 205, "Back", 10)
    f.text(x0, 218, "gauge", 10)
    f.save("press_brake")


def fig_spot_weld():
    f = Fig(600, 300)
    f.rect(230, 20, 40, 100, fill=COPPER, outline=GREY)
    f.poly([(230, 120), (270, 120), (258, 140), (242, 140)], fill=COPPER)
    f.rect(230, 180, 40, 100, fill=COPPER, outline=GREY)
    f.poly([(230, 180), (270, 180), (258, 160), (242, 160)], fill=COPPER)
    f.rect(80, 140, 340, 10, fill=STEEL)
    f.rect(80, 150, 340, 10, fill=(150, 158, 170))
    f.d.ellipse([235 * S, 143 * S, 265 * S, 157 * S], fill=(230, 120, 40))
    f.arrow(300, 30, 300, 110, RED, 3)
    f.arrow(300, 270, 300, 190, RED, 3)
    f.text(308, 60, "Electrode force", 10, True, RED)
    label(f, 250, 150, 440, 150, "Weld nugget at the sheet interface")
    label(f, 240, 60, 120, 40, "Upper electrode (Cu-Cr-Zr, water cooled)")
    label(f, 240, 240, 120, 260, "Lower electrode")
    label(f, 100, 145, 60, 110, "Two sheets")
    f.box(460, 20, 130, 60, "Transformer\n8-15 kA, few volts", fill=PINK, outline=RED, size=10)
    f.line([(460, 50), (270, 50)], ORANGE, 2)
    f.line([(525, 80), (525, 250), (270, 250)], ORANGE, 2)
    f.save("spot_weld")


def fig_mig():
    f = Fig(640, 280)
    f.box(10, 90, 120, 70, "Power source\nconstant voltage", size=10)
    f.box(170, 20, 110, 60, "Wire feeder\n(drive rolls)", fill=LORANGE, outline=ORANGE, size=10)
    f.box(170, 190, 110, 50, "Gas cylinder\nAr 82 / CO2 18", fill=LGREEN, outline=GREEN, size=10)
    f.line([(130, 110), (170, 50)], NAVY, 2)
    f.line([(280, 50), (380, 50), (420, 120)], (60, 60, 60), 5)
    f.line([(280, 215), (360, 215), (400, 120)], GREEN, 2)
    f.poly([(410, 110), (450, 110), (465, 190), (395, 190)], fill=STEEL)
    f.line([(430, 190), (430, 215)], ORANGE, 2)
    f.poly([(420, 215), (440, 215), (436, 230), (424, 230)], fill=(255, 220, 120), outline=ORANGE)
    f.rect(330, 232, 220, 14, fill=(150, 158, 170))
    f.line([(130, 140), (150, 260), (330, 245)], NAVY, 2)
    label(f, 455, 150, 500, 120, "Torch: contact tip + gas nozzle")
    label(f, 432, 222, 520, 200, "Arc and molten pool")
    label(f, 540, 240, 560, 268, "Workpiece")
    label(f, 200, 254, 90, 268, "Earth clamp")
    f.save("mig")


def fig_clinch():
    f = Fig(560, 230)
    for ox, title, pressed in ((30, "Before pressing", False), (300, "After pressing", True)):
        f.text(ox + 40, 10, title, 12, True, NAVY)
        f.rect(ox, 130, 90, 18, fill=STEEL)
        f.rect(ox + 140, 130, 90, 18, fill=STEEL)
        top = 130 if pressed else 80
        f.rect(ox + 92, top, 46, 30, fill=(205, 170, 70), outline=GREY)  # collar/head
        f.rect(ox + 100, top + 30, 30, 50, fill=(225, 195, 100), outline=GREY)  # shank
        if pressed:
            f.poly([(ox + 90, 148), (ox + 100, 160), (ox + 90, 160)], fill=STEEL)
            f.poly([(ox + 140, 148), (ox + 130, 160), (ox + 140, 160)], fill=STEEL)
    label(f, 145, 92, 200, 60, "Knurled collar")
    label(f, 60, 139, 20, 190, "Sheet")
    label(f, 395, 155, 330, 205, "Sheet metal flows into the undercut")
    f.save("clinch")


def fig_pretreatment():
    f = Fig(780, 220)
    stages = [("1", "Degrease\n55-65 C"), ("2", "Rinse"), ("3", "Pickling"), ("4", "Rinse"),
              ("5", "Activation"), ("6", "Zn phosphate\n45-55 C"), ("7", "DM rinse +\npassivation")]
    f.line([(10, 30), (770, 30)], GREY, 3)
    f.text(10, 8, "Overhead conveyor, 1.5 m/min", 10, True, NAVY)
    for i, (n, t) in enumerate(stages):
        x = 10 + i * 96
        hot = n in ("1", "6")
        f.rect(x, 60, 86, 70, fill=LORANGE if hot else BLUE, outline=ORANGE if hot else NAVY)
        f.text_c(x + 43, 95, t, 10)
        f.text_c(x + 43, 145, "Stage " + n, 10, True, NAVY)
        f.line([(x + 43, 30), (x + 43, 55)], GREY, 1)
    f.box(690, 60, 82, 70, "Dry-off\noven\n110-120 C", fill=PINK, outline=RED, size=10)
    f.text(10, 175, "Each stage: tank under the tunnel, pump, spray risers both sides; drip zones between stages.",
           10, False, (60, 60, 60))
    f.text(10, 195, "Then to powder booth PCL-09.", 10, True, NAVY)
    f.save("pretreatment")


def fig_powder():
    f = Fig(720, 280)
    f.box(10, 170, 110, 70, "Fluidising\nhopper", fill=LORANGE, outline=ORANGE, size=10)
    f.arrow(120, 200, 190, 150, ORANGE)
    f.poly([(190, 140), (260, 125), (260, 160), (190, 150)], fill=STEEL)
    f.text(180, 165, "Gun 60-80 kV", 10, True, RED)
    for k in range(6):
        f.arrow(265, 130 + k * 6, 330, 110 + k * 12, (120, 120, 200), 1)
    f.rect(335, 60, 40, 140, fill=(220, 220, 225))
    f.line([(355, 30), (355, 60)], GREY, 2)
    f.text(330, 10, "Part on earthed hook", 10, True, NAVY)
    f.box(430, 40, 110, 50, "Cyclone +\nsieve", size=10)
    f.box(430, 110, 110, 50, "Cartridge\nfilters + fan", size=10)
    f.arrow(380, 180, 430, 140, NAVY)
    f.arrow(430, 65, 120, 180, GREEN, 2)
    f.text(240, 60, "Recovered powder", 10, False, GREEN)
    f.box(580, 60, 130, 80, "Curing oven\nset 200 C\nmetal 180 C x 10 min", fill=PINK, outline=RED, size=10)
    f.arrow(540, 230, 640, 145, RED)
    f.text(430, 235, "Parts continue on conveyor", 10, False, RED)
    f.save("powder")


def fig_busbar_machine():
    f = Fig(760, 250)
    f.rect(10, 150, 740, 12, fill=STEEL)
    f.text(10, 168, "Infeed roller table, CNC gripper carriage (X)", 10, False, NAVY)
    f.rect(40, 135, 260, 14, fill=COPPER)
    f.rect(60, 120, 30, 30, fill=ORANGE)
    f.text(50, 100, "Gripper", 10, True, ORANGE)
    f.box(320, 40, 120, 100, "Punching\n8-tool magazine\n35 t", size=10)
    f.box(460, 40, 110, 100, "Shearing\n+ notching\n35 t", size=10)
    f.box(600, 40, 140, 100, "Bending\nflat / edgewise /\ntwist 35 t", fill=LORANGE, outline=ORANGE, size=10)
    f.arrow(300, 142, 320, 120)
    f.arrow(440, 90, 460, 90)
    f.arrow(570, 90, 600, 90)
    f.text(320, 200, "One hydraulic power pack and one CNC for all three stations", 10, True, NAVY)
    f.save("busbar_machine")


def fig_busbar_layout():
    f = Fig(620, 400)
    f.rect(60, 20, 260, 360, fill=(250, 250, 250), outline=GREY, width=2)
    f.text(70, 26, "Busbar chamber", 10, True, NAVY)
    cols = [("L1", (210, 50, 40)), ("L2", (220, 180, 30)), ("L3", (40, 80, 200)), ("N", (30, 30, 30))]
    for i, (n, c) in enumerate(cols):
        x = 90 + i * 45
        f.rect(x, 50, 14, 40, fill=c, outline=c)
        f.text(x, 94, n, 10, True)
    f.rect(80, 110, 220, 6, fill=STEEL)
    f.text(180, 120, "Support insulators", 9)
    for i, (n, c) in enumerate(cols[:3]):
        x = 245 + i * 20
        f.rect(x, 135, 8, 210, fill=c, outline=c)
    f.text(225, 350, "Vertical droppers", 9)
    for k in range(3):
        f.rect(80, 140 + k * 70, 140, 58, fill=BLUE, outline=NAVY)
        f.text(90, 160 + k * 70, "Functional unit %d" % (k + 1), 10)
    f.rect(70, 360, 240, 8, fill=(40, 140, 60), outline=(40, 140, 60))
    f.text(75, 370, "PE bar (green-yellow)", 9, True, GREEN)
    f.box(360, 40, 240, 120, "Clearances (Table 16-2)\nPhase-phase: 25 mm\nPhase-neutral: 25 mm\nPhase-earth: 20 mm\nTo door / cover: 25 mm",
          fill=LORANGE, outline=ORANGE, size=11)
    f.box(360, 190, 240, 100, "Joint torque (Table 16-3)\nM8 22 Nm, M10 44 Nm\nM12 75 Nm, M16 160 Nm",
          fill=LGREEN, outline=GREEN, size=11)
    f.save("busbar_layout")


def fig_dol():
    f = Fig(720, 380)
    # power circuit
    f.text(20, 6, "Power circuit", 12, True, NAVY)
    for i, n in enumerate(("L1", "L2", "L3")):
        x = 40 + i * 40
        f.text(x - 6, 22, n, 10, True)
        f.line([(x, 40), (x, 330)], (40, 40, 40), 2)
        f.rect(x - 8, 70, 16, 24, fill="white", outline=(40, 40, 40))
        f.rect(x - 8, 150, 16, 24, fill="white", outline=(40, 40, 40))
        f.rect(x - 8, 230, 16, 24, fill=LORANGE, outline=ORANGE)
    f.text(160, 76, "Q1 MPCB / MCCB", 10)
    f.text(160, 156, "K11 contactor (main contacts)", 10)
    f.text(160, 236, "F11 overload relay", 10)
    f.circle(80, 345, 22, fill=BLUE)
    f.text_c(80, 345, "M\n3~", 10, True)
    # control circuit ladder
    x0 = 400
    f.text(x0, 6, "Control circuit", 12, True, NAVY)
    f.line([(x0, 40), (x0 + 300, 40)], RED, 2)
    f.text(x0 + 230, 22, "L (from F2)", 10, True, RED)
    f.line([(x0, 350), (x0 + 300, 350)], (40, 40, 40), 2)
    f.text(x0 + 305, 342, "N", 10, True)
    rung = x0 + 60
    items = [(60, "S0 emergency stop (NC)"), (100, "S2 STOP (NC)"), (140, "F11 95-96 (NC)")]
    f.line([(rung, 40), (rung, 180)], (40, 40, 40), 2)
    for y, t in items:
        f.rect(rung - 10, y, 20, 18, fill=PINK, outline=RED)
        f.text(rung + 16, y + 2, t, 10)
    f.line([(rung, 180), (rung + 120, 180)], (40, 40, 40), 2)
    f.line([(rung, 180), (rung, 260)], (40, 40, 40), 2)
    f.rect(rung - 10, 205, 20, 18, fill=LGREEN, outline=GREEN)
    f.text(rung - 75, 207, "S1 START", 10)
    f.line([(rung + 120, 180), (rung + 120, 260)], (40, 40, 40), 2)
    f.rect(rung + 110, 205, 20, 18, fill=BLUE, outline=NAVY)
    f.text(rung + 136, 200, "K11 13-14", 10)
    f.text(rung + 136, 214, "(holding contact)", 9)
    f.line([(rung, 260), (rung + 120, 260)], (40, 40, 40), 2)
    f.line([(rung + 60, 260), (rung + 60, 290)], (40, 40, 40), 2)
    f.rect(rung + 40, 290, 40, 30, fill=BLUE, outline=NAVY)
    f.text_c(rung + 60, 305, "K11", 10, True)
    f.text(rung + 88, 298, "coil A1-A2", 10)
    f.line([(rung + 60, 320), (rung + 60, 350)], (40, 40, 40), 2)
    f.save("dol")


def fig_test_bay():
    f = Fig(640, 330)
    f.rect(20, 20, 400, 290, fill=(250, 250, 250), outline=RED, width=3)
    f.text(30, 26, "Fenced test bay (interlocked gates)", 11, True, RED)
    f.box(140, 100, 160, 140, "Panel under test", fill=BLUE, size=12, bold=True)
    f.rect(410, 140, 14, 60, fill=ORANGE, outline=ORANGE)
    f.text(390, 205, "Gate", 10, True, ORANGE)
    f.circle(400, 40, 10, fill=PINK, outline=RED)
    f.text(330, 55, "Red / green beacon", 9)
    f.box(470, 110, 150, 110, "Test desk\nHV 0-5 kV\nIR 1000 V\n10 A continuity\nInjection sets", fill=LGREEN,
          outline=GREEN, size=10)
    f.rect(470, 230, 150, 18, fill=(40, 40, 40))
    f.text(475, 252, "Insulating mat", 10)
    f.line([(300, 170), (470, 170)], NAVY, 2)
    f.text(320, 150, "Test leads", 10, False, NAVY)
    f.circle(600, 95, 9, fill=(230, 40, 40), outline=(120, 0, 0))
    f.text(520, 80, "E-stop", 10, True, RED)
    f.save("test_bay")


def fig_compressor():
    f = Fig(780, 230)
    items = [("Inlet filter +\ninlet valve", BLUE, NAVY), ("Screw element\n(oil injected)", LORANGE, ORANGE),
             ("Oil separator\ntank + element", BLUE, NAVY), ("Min. pressure\nvalve +\nafter-cooler", BLUE, NAVY),
             ("Receiver\n1000 l", LGREEN, GREEN), ("Refrigerated\ndryer +3 C", LGREEN, GREEN),
             ("Filters\n1 / 0.01 micron", LGREEN, GREEN)]
    for i, (t, fill, out) in enumerate(items):
        x = 10 + i * 110
        f.box(x, 40, 96, 74, t, fill=fill, outline=out, size=10)
        if i:
            f.arrow(x - 14, 77, x - 2, 77)
    f.line([(10 + 2 * 110 + 48, 114), (10 + 2 * 110 + 48, 170), (10 + 110 + 48, 170), (10 + 110 + 48, 116)], ORANGE, 2)
    f.box(170, 150, 150, 40, "Oil cooler + oil filter", fill=LORANGE, outline=ORANGE, size=10)
    f.text(10, 200, "Load at 7.0 bar, unload at 8.0 bar; motor stops after 5 min unloaded", 11, True, NAVY)
    f.text(560, 130, "To plant air network", 10, True, GREEN)
    f.save("compressor")


def fig_voltage_method():
    f = Fig(620, 300)
    f.line([(40, 30), (580, 30)], RED, 2)
    f.text(585, 22, "L", 11, True, RED)
    f.line([(40, 270), (580, 270)], (40, 40, 40), 2)
    f.text(585, 262, "N", 11, True)
    f.line([(120, 30), (120, 270)], (40, 40, 40), 2)
    pts = [(70, "1"), (115, "2"), (160, "3"), (205, "4")]
    names = ["E-stop", "STOP", "OL 95-96", "START / hold"]
    for (y, n), nm in zip(pts, names):
        f.rect(110, y - 8, 20, 18, fill=PINK if n != "4" else LGREEN, outline=RED if n != "4" else GREEN)
        f.text(136, y - 6, nm, 10)
    f.rect(100, 230, 40, 26, fill=BLUE, outline=NAVY)
    f.text_c(120, 243, "Coil", 10, True)
    probes = [(52, "Point A: 230 V"), (95, "Point B: 230 V"), (140, "Point C: 0 V  -> fault between B and C"),
              (225, "Coil A1")]
    for y, t in probes:
        f.circle(120, y, 4, fill=ORANGE, outline=ORANGE)
        f.line([(124, y), (300, y)], ORANGE, 1)
        f.text(305, y - 7, t, 10, True, ORANGE if "fault" not in t else RED)
    f.text(300, 250, "Black probe stays on N; red probe moves down the rung", 10, False, NAVY)
    f.save("voltage_method")


def fig_hydraulic_circuit():
    f = Fig(640, 360)
    f.rect(40, 290, 200, 50, fill=(220, 232, 245), outline=NAVY)
    f.text(110, 305, "Tank", 11, True, NAVY)
    f.circle(140, 240, 20, fill=LORANGE, outline=ORANGE)
    f.text(170, 232, "Pump + motor", 10)
    f.line([(140, 290), (140, 260)], NAVY, 2)
    f.line([(140, 220), (140, 170), (330, 170)], NAVY, 2)
    f.rect(60, 150, 50, 30, fill=PINK, outline=RED)
    f.text(20, 125, "Relief valve", 10, True, RED)
    f.line([(110, 165), (140, 165)], NAVY, 2)
    f.line([(85, 180), (85, 290)], NAVY, 1)
    f.rect(330, 140, 150, 60, fill=BLUE, outline=NAVY)
    f.line([(380, 140), (380, 200)], NAVY, 1)
    f.line([(430, 140), (430, 200)], NAVY, 1)
    f.text(335, 205, "4/3 directional valve", 10)
    f.line([(370, 140), (370, 80)], NAVY, 2)
    f.line([(440, 140), (440, 80)], NAVY, 2)
    f.rect(340, 40, 220, 40, fill=STEEL, outline=GREY)
    f.rect(440, 45, 10, 30, fill=(90, 90, 90))
    f.line([(450, 60), (600, 60)], (90, 90, 90), 6)
    f.text(480, 20, "Cylinder", 11, True)
    f.line([(480, 200), (480, 260), (240, 300)], NAVY, 2)
    f.rect(300, 250, 60, 26, fill=LGREEN, outline=GREEN)
    f.text(300, 280, "Return filter", 10, False, GREEN)
    f.circle(250, 170, 10, fill="white", outline=NAVY)
    f.text(220, 140, "Gauge", 10)
    f.save("hydraulic_circuit")


def main():
    for fn in [plant_flow, loto_steps]:
        fn()
    import sys
    mod = sys.modules[__name__]
    for name in dir(mod):
        if name.startswith("fig_"):
            getattr(mod, name)()


if __name__ == "__main__":
    main()
