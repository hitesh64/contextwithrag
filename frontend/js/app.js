'use strict';
// ContextBasedRAG frontend. Everything shown comes from the API; the browser never holds an API key
// and never decides what the user may see - the backend does.

const API = '/api/v1';
const ROLES = ['viewer', 'technician', 'maintenance_manager', 'admin'];
const ROLE_NAMES = { viewer: 'Viewer', technician: 'Technician', maintenance_manager: 'Maintenance manager', admin: 'Administrator' };
const STATUS_STYLE = {
  ready: 'ok', resolved: 'ok', approved: 'ok', completed: 'ok', active: 'ok', success: 'ok',
  queued: 'info', processing: 'info', in_progress: 'info', draft: 'info',
  pending_approval: 'warn', open: 'warn', under_maintenance: 'warn', high: 'warn', denied: 'warn',
  failed: 'bad', rejected: 'bad', critical: 'bad', conflict: 'bad', needs_review: 'warn', cancelled: '', archived: '', inactive: '',
  accepted: 'ok', pending_payment: 'warn', paid: 'ok', unpaid: 'warn',
};
const MOVE_LABEL = {
  pending_approval: 'Submit for approval', approved: 'Approve', rejected: 'Reject', draft: 'Back to draft',
  in_progress: 'Start work', completed: 'Mark completed', cancelled: 'Cancel work order',
};

let token = sessionStorage.getItem('token');
let me = null;
let charts = [];
let pollTimer = null;
const chatLog = [];

const $ = (selector, root = document) => root.querySelector(selector);
const page = () => $('#page');

// ---------- helpers ----------

function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
const label = value => esc(String(value ?? '').replace(/_/g, ' '));
const badge = value => (value ? `<span class="badge ${STATUS_STYLE[value] || ''}">${label(value)}</span>` : '');
const when = value => (value ? new Date(value).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' }) : '—');
const day = value => (value ? new Date(value).toLocaleDateString([], { dateStyle: 'medium' }) : '—');
const shown = value => (value === null || value === undefined || value === '' ? '<span class="muted">not recorded</span>' : esc(value));
// The server sends what this user may do; it enforces the same list itself, so this only decides what is drawn
const can = permission => Boolean(me) && (permission === 'platform.owner' ? me.platform_owner : me.permissions.includes(permission));

function toast(message, bad = false) {
  const el = document.createElement('div');
  el.className = 'toast' + (bad ? ' bad' : '');
  el.innerHTML = `<i class="fa-solid ${bad ? 'fa-circle-exclamation' : 'fa-circle-check'}"></i><span>${esc(message)}</span>`;
  $('#toast').append(el);
  setTimeout(() => el.remove(), bad ? 7000 : 3500);
}

async function api(path, { method = 'GET', body, form, params, raw = false } = {}) {
  let url = API + path;
  if (params) {
    const query = new URLSearchParams(Object.entries(params).filter(([, v]) => v !== '' && v !== null && v !== undefined));
    if (query.toString()) url += '?' + query;
  }
  const headers = {};
  if (token) headers.Authorization = 'Bearer ' + token;
  let payload = form;
  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
    payload = JSON.stringify(body);
  }
  let response;
  try {
    response = await fetch(url, { method, headers, body: payload });
  } catch {
    throw new Error('Cannot reach the server. Check that it is running.');
  }
  if (response.status === 401 && token) {
    signOut();
    throw new Error('Your login has expired. Sign in again.');
  }
  if (response.status === 402 && token && me) {
    // The company's registration payment was withdrawn while this page was open
    me.organization_status = 'pending_payment';
    showPayment();
    throw new Error('The registration payment of your company is not confirmed.');
  }
  if (!response.ok) {
    let message = response.statusText || 'Request failed';
    try {
      const detail = (await response.json()).detail;
      message = typeof detail === 'string' ? detail : detail.map(e => `${e.loc.slice(1).join('.')}: ${e.msg}`).join('; ');
    } catch { /* not JSON: keep the status text */ }
    throw new Error(message);
  }
  if (raw) return response;
  return response.status === 204 ? null : response.json();
}

/** Run an action and show its error, so no failure is ever silent. */
async function attempt(action, success) {
  try {
    const result = await action();
    if (success) toast(success);
    return result;
  } catch (error) {
    toast(error.message, true);
    return undefined;
  }
}

function table(columns, rows, { empty = 'Nothing here yet.', rowLink } = {}) {
  if (!rows.length) return `<div class="empty">${esc(empty)}</div>`;
  const head = columns.map(c => `<th class="${c.num ? 'num' : ''}">${esc(c.title)}</th>`).join('');
  const body = rows.map(row => {
    const cells = columns.map(c => `<td class="${c.num ? 'num' : ''}">${c.cell(row)}</td>`).join('');
    return rowLink ? `<tr class="clickable" data-href="${esc(rowLink(row))}">${cells}</tr>` : `<tr>${cells}</tr>`;
  }).join('');
  return `<div class="table-wrap"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
}

function pager(data, name) {
  const pages = Math.max(1, Math.ceil(data.total / data.page_size));
  if (pages <= 1) return `<div class="pager">${data.total} record${data.total === 1 ? '' : 's'}</div>`;
  return `<div class="pager">${data.total} records · page ${data.page} of ${pages}
    <button class="btn small" data-action="${name}" data-page="${data.page - 1}" ${data.page <= 1 ? 'disabled' : ''}>Previous</button>
    <button class="btn small" data-action="${name}" data-page="${data.page + 1}" ${data.page >= pages ? 'disabled' : ''}>Next</button></div>`;
}

/**
 * A form in a dialog. fields: {name, label, type, value, options, required, hint, multiple, accept}.
 * submit(values) may throw: the message is shown and the dialog stays open.
 */
function formDialog({ title, fields = [], submitLabel = 'Save', note = '', tone = '', submit }) {
  return new Promise(resolve => {
    const dialog = document.createElement('dialog');
    dialog.className = tone ? `confirm tone-${tone}` : fields.length > 6 ? 'wide' : fields.length ? '' : 'narrow';
    const icon = tone ? { danger: 'fa-triangle-exclamation', warn: 'fa-circle-exclamation', info: 'fa-circle-question' }[tone] : 'fa-pen-to-square';
    const inputs = fields.map(f => {
      const required = f.required ? 'required' : '';
      let input;
      if (f.type === 'select') {
        const options = f.options.map(o => {
          const [value, text] = Array.isArray(o) ? o : [o, String(o).replace(/_/g, ' ')];
          const selected = (f.multiple ? (f.value || []).includes(value) : value === f.value) ? 'selected' : '';
          return `<option value="${esc(value)}" ${selected}>${esc(text)}</option>`;
        }).join('');
        input = `<select name="${f.name}" ${required} ${f.multiple ? 'multiple' : ''}>${options}</select>`;
      } else if (f.type === 'checks') {
        return `<fieldset class="checks"><legend>${esc(f.label)}</legend>${f.options.map(([value, text]) =>
          `<label class="check"><input type="checkbox" name="${f.name}" value="${esc(value)}" ${(f.value || []).includes(value) ? 'checked' : ''}>${esc(text)}</label>`).join('')}</fieldset>`;
      } else if (f.type === 'textarea') {
        input = `<textarea name="${f.name}" rows="${f.rows || 4}" ${required} maxlength="${f.maxlength || 5000}">${esc(f.value)}</textarea>`;
      } else {
        const extra = [f.accept ? `accept="${f.accept}"` : '', f.min !== undefined ? `min="${f.min}"` : '', f.minlength ? `minlength="${f.minlength}"` : ''].join(' ');
        input = `<input name="${f.name}" type="${f.type || 'text'}" value="${esc(f.value)}" ${required} ${extra}>`;
      }
      return `<label>${esc(f.label)}${f.required ? ' *' : ''}${input}${f.hint ? `<span class="hint">${esc(f.hint)}</span>` : ''}</label>`;
    }).join('');
    dialog.innerHTML = `<form method="dialog">
      <div class="modal-header"><h2><i class="fa-solid ${icon}"></i>${esc(title)}</h2>
        <button type="button" class="modal-close" data-cancel aria-label="Close">&times;</button></div>
      <div class="modal-body">${note ? `<p class="hint">${esc(note)}</p>` : ''}${inputs}<p class="error" role="alert"></p></div>
      <div class="modal-footer"><button type="button" class="btn" data-cancel>Cancel</button>
      <button type="submit" class="btn primary ${tone === 'danger' ? 'danger' : ''}">${esc(submitLabel)}</button></div></form>`;
    document.body.append(dialog);
    const form = $('form', dialog);
    const close = result => { dialog.close(); dialog.remove(); resolve(result); };
    dialog.querySelectorAll('[data-cancel]').forEach(button => { button.onclick = () => close(null); });
    dialog.addEventListener('cancel', event => { event.preventDefault(); close(null); });
    form.onsubmit = async event => {
      event.preventDefault();
      const values = {};
      for (const f of fields) {
        const el = form.elements[f.name];
        if (f.type === 'checks') values[f.name] = [...form.querySelectorAll(`input[name="${f.name}"]:checked`)].map(i => i.value);
        else if (f.type === 'file') values[f.name] = el.files[0];
        else if (f.multiple) values[f.name] = [...el.selectedOptions].map(o => o.value);
        else if (f.type === 'number') values[f.name] = el.value === '' ? null : Number(el.value);
        else values[f.name] = el.value.trim();
      }
      const button = $('[type=submit]', form);
      button.disabled = true;
      try {
        close(await submit(values) ?? true);
      } catch (error) {
        $('.error', form).textContent = error.message;
        button.disabled = false;
      }
    };
    dialog.showModal();
  });
}

const confirmDialog = (title, note, submitLabel = 'Confirm', tone = 'info') =>
  formDialog({ title, note, submitLabel, tone, submit: async () => true });

async function assetOptions() {
  const found = await api('/assets/options');
  return found.map(a => [a.id, `${a.asset_code} — ${a.name}`]);
}

/** Hand a file that came through the authenticated API to the browser, to keep under this name. */
function saveFile(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}

/** Open an original document through the authenticated API (there is no public file URL). */
async function openDocument(id, pageNumber) {
  await attempt(async () => {
    const response = await api(`/documents/${id}/file`, { raw: true });
    const blob = await response.blob();
    if (!/pdf|^text\//.test(blob.type)) {
      // A browser cannot show a spreadsheet or an Office file in a tab: it is saved under its own name instead
      const name = /filename\*?=(?:UTF-8'')?"?([^";]+)/i.exec(response.headers.get('content-disposition') || '');
      saveFile(blob, name ? decodeURIComponent(name[1]) : 'document');
      return;
    }
    const url = URL.createObjectURL(blob);
    window.open(url + (pageNumber ? `#page=${pageNumber}` : ''), '_blank', 'noopener');
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  });
}

/** Download a register as an Excel file, with the filters the list is showing. */
const exportExcel = (path, params, filename) => attempt(async () => {
  const response = await api(path, { params, raw: true });
  saveFile(await response.blob(), filename);
}, 'Excel file downloaded');

function locator(source) {
  if (source.page) return `page ${source.page}`;
  if (source.section) return `section “${source.section}”`;
  return 'location not available';
}

function sourceList(sources) {
  if (!sources.length) return '';
  return `<div class="sources">${sources.map(s => s.type === 'breakdown'
    ? `<div class="source"><span><b>[${s.n}]</b> Breakdown record <a href="#/breakdowns?asset=${esc(s.asset_code)}">${esc(s.record_no)}</a> · ${esc(s.asset_code)} · ${day(s.reported_at)}</span><span class="excerpt">${esc(s.excerpt)}</span></div>`
    : `<div class="source"><span><b>[${s.n}]</b> <a href="#" data-action="open-doc" data-id="${esc(s.document_id)}" data-page="${esc(s.page || '')}">${esc(s.filename)}</a> · ${esc(locator(s))}</span><span class="excerpt">${esc(s.excerpt)}</span></div>`
  ).join('')}</div>`;
}

const withRefs = text => esc(text).replace(/\[(\d+(?:, \d+)*)\]/g, '<span class="cite-ref">[$1]</span>');

// ---------- pages ----------

// [page, label, permission that makes the section visible, icon, sidebar section]
const NAV = [
  ['dashboard', 'Dashboard', 'dashboard.view', 'gauge-high', 'Main'], ['chat', 'Ask', 'chat.ask', 'comments', 'Main'],
  ['assets', 'Assets', 'assets.view', 'industry', 'Maintenance'], ['documents', 'Documents', 'documents.view', 'book-open', 'Maintenance'],
  ['breakdowns', 'Breakdowns', 'breakdowns.view', 'triangle-exclamation', 'Maintenance'], ['work-orders', 'Work orders', 'work_orders.view', 'clipboard-list', 'Maintenance'],
  ['conflicts', 'Conflicts', 'conflicts.view', 'code-compare', 'Maintenance'],
  ['audit', 'Audit history', 'audit.view', 'clock-rotate-left', 'Administration'], ['users', 'Users', 'users.manage', 'users', 'Administration'],
  ['payments', 'Payments', 'platform.owner', 'indian-rupee-sign', 'Platform'],
];
const fa = name => `<i class="fa-solid fa-${name}"></i>`;

/** Count pills in the sidebar, from the same figures the dashboard shows. */
function navBadges(d) {
  const counts ={ 'work-orders': d.work_orders.pending_approval || 0, breakdowns: (d.breakdowns.open || 0) + (d.breakdowns.in_progress || 0) };
  for (const [key, count] of Object.entries(counts)) {
    const link = $(`#nav a[data-page="${key}"]`);
    if (!link) continue;
    $('.nav-badge', link)?.remove();
    if (count) link.insertAdjacentHTML('beforeend', `<span class="nav-badge">${count}</span>`);
  }
}
const pages = {};
let actions = {};

// Dashboard: plant health (availability, MTTR, MTBF, downtime), the counters, the breakdown trend and status,
// downtime by asset, the work order pipeline, what needs attention, and how well the library answers questions.
// Every figure comes from /dashboard, counted from this factory's own records.
const WO_STAGES = [['draft', 'Draft'], ['pending_approval', 'Awaiting approval'], ['approved', 'Approved'], ['in_progress', 'In progress'], ['completed', 'Completed']];
const PRIORITY_TONE = { critical: 'bad', high: 'warn', medium: 'info', low: '' };
const plural = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;
const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

const duration = minutes => minutes >= 60 ? [minutes / 60, 'h', 1] : [minutes, 'min', 0];
const longSpan = hours => hours >= 72 ? [hours / 24, 'days', 1] : [hours, 'h', 1];

// Numbers count up from zero once the cards are on the page
function countUp(root) {
  for (const el of root.querySelectorAll('[data-count]')) {
    const target = Number(el.dataset.count);
    const decimals = Number(el.dataset.decimals || 0);
    const show = v => { el.textContent = v.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals }); };
    if (reduceMotion() || !Number.isFinite(target)) { show(target); continue; }
    const start = performance.now();
    const step = t => {
      const p = Math.min(1, (t - start) / 1100);
      show(target * (1 - (1 - p) ** 3));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }
}

function kpiTile({ tone, icon, label, value, unit, decimals = 0, sub, info, ring }) {
  const number = value === null || value === undefined
    ? '<span class="kpi-none">—</span>'
    : `<span data-count="${value}" data-decimals="${decimals}">0</span><small>${esc(unit)}</small>`;
  return `<div class="kpi tone-${tone}" title="${esc(info)}">
    ${ring !== undefined ? `<svg class="kpi-ring" viewBox="0 0 120 120" aria-hidden="true"><circle class="track" cx="60" cy="60" r="52"/>
      ${ring ? `<circle class="fill" cx="60" cy="60" r="52" pathLength="100" style="--p:${ring}"/>` : ''}</svg>` : ''}
    <div class="kpi-top"><span class="kpi-icon">${fa(icon)}</span><span class="kpi-label">${esc(label)}</span>${fa('circle-info kpi-info')}</div>
    <div class="kpi-value">${number}</div>
    <div class="kpi-sub">${sub}</div>
  </div>`;
}

// No machines yet: the figures cannot exist, so say what to record instead of showing dashes
function plantSetup() {
  const step = (n, icon, title, text, href, label, allowed) => `<div class="setup-step" style="--i:${n}">
    <span class="setup-n">${n}</span><span class="setup-icon">${fa(icon)}</span>
    <div><b>${title}</b><p>${text}</p></div>
    ${allowed ? `<a class="btn small" href="${href}">${label}${fa('arrow-right')}</a>` : ''}</div>`;
  return `<section class="dash-section">
    <div class="section-head"><h2>${fa('heart-pulse')}Plant health</h2><span class="hint">Availability, MTTR, MTBF and downtime appear here</span></div>
    <div class="plant-setup">
      <div class="setup-intro">${fa('chart-line')}<div><b>No machines recorded yet</b>
        <p>These figures are counted from your own records. Add your machines and record their breakdowns, with the downtime in minutes.</p></div></div>
      <div class="setup-steps">
        ${step(1, 'industry', 'Add your machines', 'One asset per machine, with its criticality.', '#/assets?open=add-asset', 'Add asset', can('assets.manage'))}
        ${step(2, 'triangle-exclamation', 'Record breakdowns', 'When a machine stops: what happened and the downtime in minutes.', '#/breakdowns?open=add-breakdown', 'Report breakdown', can('breakdowns.report'))}
        ${step(3, 'file-import', 'Or import your log', 'An Excel or CSV breakdown register you already keep.', '#/breakdowns?open=import', 'Import', can('breakdowns.import'))}
      </div></div></section>`;
}

function plantHealth(d) {
  const k = d.kpis;
  if (!k.assets_in_service) return plantSetup();
  const [mttr, mttrUnit, mttrDec] = k.mttr_minutes === null ? [null, '', 0] : duration(k.mttr_minutes);
  const [mtbf, mtbfUnit, mtbfDec] = k.mtbf_hours === null ? [null, '', 0] : longSpan(k.mtbf_hours);
  const none = k.breakdowns ? 'No downtime minutes recorded on the breakdowns' : 'No breakdowns in this period';
  return `<section class="dash-section">
    <div class="section-head"><h2>${fa('heart-pulse')}Plant health</h2>
      <span class="hint">${plural(k.assets_in_service, 'asset')} in service · ${plural(k.breakdowns, 'breakdown')} in ${d.period_days} days · round-the-clock basis</span></div>
    <div class="kpi-row">
      ${kpiTile({ tone: 'green', icon: 'gauge-high', label: 'Availability', value: k.availability_pct, unit: '%', decimals: 1, ring: k.availability_pct,
        sub: k.availability_pct === null ? 'Add assets to measure it' : 'Uptime of the assets in service',
        info: 'Calendar hours of the assets in service (not inactive), minus recorded downtime, as a share of the calendar hours. Plant schedules are not recorded, so assets count as running round the clock.' })}
      ${kpiTile({ tone: 'blue', icon: 'screwdriver-wrench', label: 'MTTR', value: mttr, unit: mttrUnit, decimals: mttrDec,
        sub: mttr === null ? none : 'Mean time to repair: downtime per breakdown',
        info: 'Mean time to repair: the average recorded downtime of the breakdowns in this period. Records without a downtime value are left out.' })}
      ${kpiTile({ tone: 'purple', icon: 'clock-rotate-left', label: 'MTBF', value: mtbf, unit: mtbfUnit, decimals: mtbfDec,
        sub: mtbf === null ? none : 'Mean time between failures',
        info: 'Mean time between failures: running hours of the assets in service (round the clock, minus downtime) divided by the number of breakdowns in this period.' })}
      ${kpiTile({ tone: 'amber', icon: 'hourglass-half', label: 'Downtime', value: Math.round(k.downtime_minutes / 6) / 10, unit: 'h', decimals: 1,
        sub: `${sparkline(d.trend.map(b => b.downtime_minutes))}<span>${plural(k.breakdowns, 'breakdown')}</span>`,
        info: 'Total recorded downtime of the breakdowns reported in this period.' })}
    </div>
  </section>`;
}

function sparkline(values) {
  const max = Math.max(1, ...values);
  if (values.length < 2) return '';
  const points = values.map((v, i) => `${(i / (values.length - 1)) * 100},${28 - (v / max) * 26}`).join(' ');
  return `<svg class="spark" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true">
    <polygon points="0,30 ${points} 100,30"/><polyline points="${points}"/></svg>`;
}

function cycleText(hours) {
  if (hours === null) return 'No orders completed in this period';
  const [value, unit] = longSpan(hours);
  return `Average <b>${value.toFixed(1)} ${unit}</b> from creation to completion`;
}

function pipeline(d) {
  const counts = WO_STAGES.map(([key]) => d.work_orders[key] || 0);
  const max = Math.max(1, ...counts);
  const open = d.work_orders_open_by_priority;
  return `<div class="card dash-card" style="--d:4"><h2>${fa('diagram-next')}Work order pipeline</h2>
    <div class="pipe">${WO_STAGES.map(([key, text], i) => `
      <a class="pipe-row" href="#/work-orders?status=${key}" style="--i:${i}">
        <span class="pipe-name">${text}</span>
        <span class="pipe-bar"><span style="--w:${(counts[i] / max) * 100}%"></span></span>
        <b data-count="${counts[i]}">0</b></a>`).join('')}</div>
    <div class="pipe-foot">
      <div class="prio">${['critical', 'high', 'medium', 'low'].map(p => `<span class="badge ${PRIORITY_TONE[p]}">${open[p] || 0} ${p}</span>`).join('')}
        <span class="hint">open, by priority</span></div>
      <div class="cycle">${fa('stopwatch')}${cycleText(d.work_order_cycle_hours)}</div>
    </div></div>`;
}

function attention(d) {
  const rows = d.attention.map(a => `<a class="att-row" href="#/breakdowns?status=open&q=${encodeURIComponent(a.asset_code)}">
      <span class="crit crit-${esc(a.criticality)}" title="${esc(a.criticality)} criticality"></span>
      <span class="att-name"><b>${esc(a.asset_code)}</b><span>${esc(a.name)}</span></span>
      ${a.status === 'under_maintenance' ? badge('under_maintenance') : ''}
      ${a.unresolved_breakdowns ? `<span class="badge bad">${plural(a.unresolved_breakdowns, 'open breakdown')}</span>` : ''}</a>`).join('');
  return `<div class="card dash-card" style="--d:5"><h2>${fa('bell')}Needs attention</h2>
    ${rows ? `<div class="att">${rows}</div>` : `<div class="all-clear">${fa('circle-check')}<b>All clear</b><span>No open breakdowns and no asset under maintenance.</span></div>`}</div>`;
}

function failures(d) {
  const maxCode = Math.max(1, ...d.top_error_codes.map(c => c.breakdowns));
  return `<div class="card dash-card" style="--d:6"><h2>${fa('repeat')}Repeat failures</h2>
    ${d.repeat_assets.length ? `<div class="mini-list">${d.repeat_assets.map(a => `<a href="#/breakdowns?q=${encodeURIComponent(a.asset_code)}">
      <span><b>${esc(a.asset_code)}</b> ${esc(a.name)}</span><span class="badge warn">${a.breakdowns}×</span></a>`).join('')}</div>`
      : '<p class="hint">No asset broke down twice in this period.</p>'}
    <h3>${fa('barcode')}Most frequent fault codes</h3>
    ${d.top_error_codes.length ? `<div class="codes">${d.top_error_codes.map((c, i) => `<a href="#/breakdowns?error_code=${encodeURIComponent(c.error_code)}" style="--i:${i}">
      <code>${esc(c.error_code)}</code><span class="code-bar"><span style="--w:${(c.breakdowns / maxCode) * 100}%"></span></span><b>${c.breakdowns}</b></a>`).join('')}</div>`
      : '<p class="hint">No fault codes recorded in this period.</p>'}</div>`;
}

function knowledge(d) {
  const answered = d.questions_asked ? Math.round(100 * (d.questions_asked - d.questions_unanswered) / d.questions_asked) : null;
  return `<div class="card dash-card" style="--d:7"><h2>${fa('brain')}Knowledge base</h2>
    <div class="know">
      <div class="know-ring"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="track" cx="60" cy="60" r="50"/>
        ${answered ? `<circle class="fill" cx="60" cy="60" r="50" pathLength="100" style="--p:${answered}"/>` : ''}</svg>
        <div><b>${answered === null ? '—' : `<span data-count="${answered}">0</span>%`}</b><span>answered</span></div></div>
      <dl class="know-facts">
        <dt>Questions asked</dt><dd data-count="${d.questions_asked}">0</dd>
        <dt>Without evidence</dt><dd data-count="${d.questions_unanswered}">0</dd>
        ${can('documents.view') ? `<dt>Documents ready</dt><dd data-count="${d.documents.ready || 0}">0</dd>
        <dt>Failed processing</dt><dd data-count="${d.documents.failed || 0}">0</dd>` : ''}
      </dl></div>
    <p class="hint">${answered === null ? 'No questions asked in this period yet.' : 'Share of questions answered from your own manuals, SOPs and records.'}</p></div>`;
}

pages.dashboard = async (_, query) => {
  const days = query.get('days') || '90';
  const d = await api('/dashboard', { params: { days } });
  const sum = counts => Object.values(counts).reduce((a, b) => a + b, 0);
  const stat = (value, text, href, tone, icon) => `<a class="stat tone-${tone}" href="${href}"><div class="stat-icon">${fa(icon)}</div>
    <div class="label">${esc(text)}</div><div class="value" data-count="${value}">0</div><div class="stat-art" aria-hidden="true">${fa(icon)}</div></a>`;
  navBadges(d);
  const period = `${day(d.period_start)} – ${day(new Date())}`;
  const seeBreakdowns = can('breakdowns.view');
  const status = ['open', 'in_progress', 'resolved'].map(s => d.breakdowns[s] || 0);
  page().innerHTML = `<div class="dash" id="dash">
    ${orgHero()}
    <div class="page-head"><h1>${fa('gauge-high')}Dashboard</h1>
      <label>Period <select id="days">${[['30', 'Last 30 days'], ['90', 'Last 90 days'], ['365', 'Last 12 months']].map(([v, t]) => `<option value="${v}" ${v === days ? 'selected' : ''}>${t}</option>`).join('')}</select></label></div>
    ${seeBreakdowns ? plantHealth(d) : ''}
    <div class="grid dash-counters">
      ${can('assets.view') ? stat(sum(d.assets) - (d.assets.archived || 0), 'Assets in the register', '#/assets', 'blue', 'industry') : ''}
      ${can('documents.view') ? stat(d.documents.ready || 0, 'Documents ready to search', '#/documents', 'green', 'book-open')
        + stat(d.documents.failed || 0, 'Documents that failed processing', '#/documents?status=failed', 'red', 'file-circle-xmark') : ''}
      ${seeBreakdowns ? stat(status[0] + status[1], 'Unresolved breakdowns', '#/breakdowns?status=open', 'amber', 'triangle-exclamation') : ''}
      ${can('work_orders.view') ? stat(d.work_orders.pending_approval || 0, 'Work orders awaiting approval', '#/work-orders?status=pending_approval', 'purple', 'clipboard-check') : ''}
      ${stat(d.questions_unanswered, `Questions without evidence (${period})`, '#/dashboard', 'teal', 'circle-question')}
    </div>
    ${seeBreakdowns ? `<div class="dash-grid wide">
      <div class="card dash-card" style="--d:1"><h2>${fa('chart-line')}Breakdown trend</h2>
        <p class="hint">Breakdowns reported per ${d.trend_step_days === 1 ? 'day' : 'week'} and their downtime, ${esc(period)}.</p>
        ${d.kpis.breakdowns ? '<div class="chart-box sm"><canvas id="trend" aria-label="Breakdown trend" role="img"></canvas></div>' : '<div class="empty">No breakdowns recorded in this period.</div>'}</div>
      <div class="card dash-card" style="--d:2"><h2>${fa('chart-pie')}Breakdown status</h2>
        ${sum(d.breakdowns) ? `<div class="donut"><canvas id="status" aria-label="Breakdowns by status" role="img"></canvas>
          <div class="donut-center"><b data-count="${sum(d.breakdowns)}">0</b><span>records</span></div></div>
          <div class="legend">${[['open', 'Open', '#ef4444'], ['in_progress', 'In progress', '#f59e0b'], ['resolved', 'Resolved', '#10b981']].map(([key, text, colour], i) =>
            `<a href="#/breakdowns?status=${key}"><i style="background:${colour}"></i>${text}<b>${status[i]}</b></a>`).join('')}</div>`
          : '<div class="empty">No breakdowns recorded yet.</div>'}</div>
    </div>` : ''}
    <div class="dash-grid">
      ${seeBreakdowns ? `<div class="card dash-card" style="--d:3"><h2>${fa('chart-bar')}Downtime by asset</h2>
        <p class="hint">Where the hours went, ${esc(period)}. Records without a downtime value count as 0.</p>
        ${d.downtime_by_asset.length ? '<div class="chart-box sm"><canvas id="downtime" aria-label="Downtime by asset" role="img"></canvas></div>' : '<div class="empty">No breakdowns recorded in this period.</div>'}</div>` : ''}
      ${can('work_orders.view') ? pipeline(d) : ''}
    </div>
    <div class="dash-grid three">
      ${seeBreakdowns ? attention(d) + failures(d) : ''}
      ${knowledge(d)}
    </div>
    ${can('dashboard.unanswered') ? `<div class="card dash-card" id="unanswered" style="--d:8"><h2>${fa('circle-question')}Questions the records could not answer</h2>
      <p class="hint">Each one points at a manual, SOP or record that is missing from the library.</p><div id="unanswered-list"></div></div>` : ''}
  </div>`;
  $('#days').onchange = event => { location.hash = `#/dashboard?days=${event.target.value}`; };
  heroMotion();
  countUp($('#dash'));
  // Rings and bars grow from zero once the page has been drawn
  requestAnimationFrame(() => requestAnimationFrame(() => $('#dash')?.classList.add('ready')));
  // After the web font: Chart.js measures (and keeps) label widths when a chart is made
  document.fonts.ready.then(() => { if ($('#dash')) drawDashboardCharts(d); });

  if (can('dashboard.unanswered')) {
    const missing = await api('/chat/unanswered', { params: { page_size: 10 } });
    $('#unanswered-list').innerHTML = table([
      { title: 'Asked', cell: q => when(q.created_at) }, { title: 'By', cell: q => esc(q.user_name) }, { title: 'Question', cell: q => esc(q.question) },
    ], missing.items, { empty: 'No unanswered questions so far.' });
  }
};

function drawDashboardCharts(d) {
  if (!window.Chart) {
    // The chart library could not be loaded: the downtime figures as a table, the rest is already in numbers
    const box = $('#downtime')?.parentElement;
    if (box) box.outerHTML = table([
      { title: 'Asset', cell: a => esc(a.asset_code) }, { title: 'Downtime (min)', num: true, cell: a => a.downtime_minutes },
      { title: 'Breakdowns', num: true, cell: a => a.breakdowns },
    ], d.downtime_by_asset);
    return;
  }
  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
  Chart.defaults.color = '#64748b';
  const grid = { color: 'rgba(15, 23, 42, .05)' };
  const fade = (ctx, top, bottom) => {
    const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, ctx.chart.height);
    g.addColorStop(0, top); g.addColorStop(1, bottom);
    return g;
  };
  const trend = $('#trend');
  if (trend) {
    const labels = d.trend.map(b => new Date(b.start).toLocaleDateString([], { day: 'numeric', month: 'short' }));
    charts.push(new Chart(trend, {
      data: {
        labels,
        datasets: [
          { type: 'line', label: 'Downtime (h)', yAxisID: 'hours', data: d.trend.map(b => +(b.downtime_minutes / 60).toFixed(1)),
            borderColor: '#f59e0b', borderWidth: 2.5, tension: .4, pointRadius: 0, pointHoverRadius: 5, fill: true,
            backgroundColor: ctx => fade(ctx, 'rgba(245, 158, 11, .28)', 'rgba(245, 158, 11, 0)') },
          { type: 'bar', label: 'Breakdowns', yAxisID: 'count', data: d.trend.map(b => b.breakdowns),
            backgroundColor: ctx => fade(ctx, 'rgba(99, 102, 241, .9)', 'rgba(99, 102, 241, .35)'), borderRadius: 6, maxBarThickness: 16 },
        ],
      },
      options: {
        maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
        animation: { duration: 1100, easing: 'easeOutQuart' },
        plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, boxWidth: 8 } } },
        scales: {
          x: { grid: { display: false }, ticks: { maxTicksLimit: 10 } },
          count: { position: 'left', beginAtZero: true, ticks: { precision: 0 }, grid, title: { display: true, text: 'Breakdowns' } },
          hours: { position: 'right', beginAtZero: true, grid: { display: false }, title: { display: true, text: 'Downtime (h)' } },
        },
      },
    }));
  }
  const status = $('#status');
  if (status) {
    charts.push(new Chart(status, {
      type: 'doughnut',
      data: { labels: ['Open', 'In progress', 'Resolved'], datasets: [{ data: ['open', 'in_progress', 'resolved'].map(s => d.breakdowns[s] || 0),
        backgroundColor: ['#ef4444', '#f59e0b', '#10b981'], borderWidth: 3, borderColor: '#fff', hoverOffset: 8 }] },
      options: { cutout: '72%', maintainAspectRatio: false, animation: { animateRotate: true, duration: 1200 }, plugins: { legend: { display: false } } },
    }));
  }
  const downtime = $('#downtime');
  if (downtime) {
    charts.push(new Chart(downtime, {
      type: 'bar',
      data: {
        labels: d.downtime_by_asset.map(a => a.asset_code),
        datasets: [{ label: 'Downtime (h)', data: d.downtime_by_asset.map(a => +(a.downtime_minutes / 60).toFixed(1)), borderRadius: 7, maxBarThickness: 20,
          backgroundColor: ctx => { const g = ctx.chart.ctx.createLinearGradient(0, 0, ctx.chart.width, 0); g.addColorStop(0, '#6366f1'); g.addColorStop(1, '#ec4899'); return g; } }],
      },
      options: {
        indexAxis: 'y', maintainAspectRatio: false, animation: { duration: 1100, easing: 'easeOutQuart' },
        plugins: { legend: { display: false }, tooltip: { callbacks: {
          title: items => { const a = d.downtime_by_asset[items[0].dataIndex]; return `${a.asset_code} ${d.asset_names[a.asset_code] || ''}`; },
          afterLabel: ctx => plural(d.downtime_by_asset[ctx.dataIndex].breakdowns, 'breakdown') } } },
        scales: { x: { beginAtZero: true, grid, title: { display: true, text: 'Downtime (hours)' } }, y: { grid: { display: false } } },
      },
    }));
  }
}

pages.chat = async (_, query) => {
  const options = await assetOptions();
  const preset = query.get('asset') || '';
  page().innerHTML = `
    <div class="page-head"><h1>Ask your factory records</h1></div>
    <div class="notice">Answers come only from your uploaded documents and breakdown records, with the source shown under each answer.
      If the records do not contain the answer, you are told so instead of getting a guess. Each question is answered on its own.</div>
    <div id="chat-log" class="chat-log"></div>
    <form id="ask" class="card ask">
      <div class="ask-row">
        <label>Asset (optional)<select name="asset_id"><option value="">All assets and documents</option>
          ${options.map(([id, text]) => `<option value="${esc(id)}" ${id === preset ? 'selected' : ''}>${esc(text)}</option>`).join('')}</select></label>
      </div>
      <label>Question<textarea name="question" rows="3" required minlength="2" maxlength="2000" placeholder="e.g. What does alarm E-204 mean on CNC-01 and has it happened before?"></textarea></label>
      <div class="actions"><button class="btn primary" type="submit">Ask</button><span class="hint">Selecting an asset limits the search to its documents and adds its breakdown history.</span></div>
    </form>`;
  const draw = () => {
    $('#chat-log').innerHTML = chatLog.map(m => m.question !== undefined
      ? `<div class="msg question"><div class="text">${esc(m.question)}</div>${m.asset ? `<div class="hint">Asset: ${esc(m.asset)}</div>` : ''}</div>`
      : `<div class="msg ${m.insufficient_evidence ? 'unsupported' : m.conflict || m.review_required ? 'conflict' : ''}">
          ${m.insufficient_evidence ? '<div><span class="badge warn">No supporting evidence found</span></div>' : ''}
          ${m.conflict ? `<div class="conflict-head">${fa('triangle-exclamation')}Conflicting procedures detected</div>` : ''}
          ${m.review_required && !m.conflict ? `<div class="conflict-head">${fa('triangle-exclamation')}Review needed: sources may disagree</div>` : ''}
          ${(m.superseded_sources || []).length ? `<div class="hint">Superseded revision also found: ${m.superseded_sources.map(s => esc(s.filename)).join(', ')}</div>` : ''}
          <div class="text">${withRefs(m.answer)}</div>${sourceList(m.citations)}
          ${(m.conflicts || []).length ? `<div class="hint"><a href="#/conflicts?status=">Open this in Conflicts</a> to see or record the decision.</div>` : ''}
          <div class="hint">Request ${esc(m.request_id)}</div></div>`).join('');
  };
  draw();
  $('#ask').onsubmit = async event => {
    event.preventDefault();
    const form = event.target;
    const question = form.question.value.trim();
    const asset_id = form.asset_id.value || null;
    const button = $('button', form);
    button.disabled = true;
    button.textContent = 'Searching the records…';
    const result = await attempt(() => api('/chat', { method: 'POST', body: { question, asset_id } }));
    button.disabled = false;
    button.textContent = 'Ask';
    if (!result) return;
    chatLog.push({ question, asset: asset_id ? form.asset_id.selectedOptions[0].textContent : '' }, result);
    form.question.value = '';
    draw();
    $('#chat-log').lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
};

const ASSET_FIELDS = asset => [
  { name: 'name', label: 'Name', required: true, value: asset.name, minlength: 2 },
  { name: 'asset_type', label: 'Type', value: asset.asset_type, hint: 'e.g. CNC lathe, hydraulic press, compressor' },
  { name: 'manufacturer', label: 'Manufacturer', value: asset.manufacturer },
  { name: 'model', label: 'Model', value: asset.model },
  { name: 'serial_number', label: 'Serial number', value: asset.serial_number },
  { name: 'location', label: 'Location', value: asset.location },
  { name: 'criticality', label: 'Criticality', type: 'select', options: ['low', 'medium', 'high', 'critical'], value: asset.criticality || 'medium' },
  { name: 'status', label: 'Status', type: 'select', options: ['active', 'under_maintenance', 'inactive'], value: asset.status === 'archived' ? 'inactive' : asset.status || 'active' },
];

pages.assets = async (id, query) => {
  if (id) return assetDetail(id);
  const params = { q: query.get('q') || '', status: query.get('status') || '', page: query.get('page') || 1 };
  const data = await api('/assets', { params });
  page().innerHTML = `
    <div class="page-head"><h1>Asset register</h1><div class="actions">
      <button class="btn" data-action="export-assets">Export Excel</button>
      ${can('assets.manage') ? '<button class="btn primary" data-action="add-asset">Add asset</button>' : ''}</div></div>
    <form class="filters" id="filters">
      <label>Search<input name="q" value="${esc(params.q)}" placeholder="Code, name, location…"></label>
      <label>Status<select name="status">${[['', 'In use (not archived)'], ['active', 'Active'], ['under_maintenance', 'Under maintenance'], ['inactive', 'Inactive'], ['archived', 'Archived']].map(([v, t]) => `<option value="${v}" ${v === params.status ? 'selected' : ''}>${t}</option>`).join('')}</select></label>
      <button class="btn" type="submit">Apply</button>
    </form>
    ${table([
      { title: 'Code', cell: a => `<b>${esc(a.asset_code)}</b>` }, { title: 'Name', cell: a => esc(a.name) },
      { title: 'Type', cell: a => esc(a.asset_type) }, { title: 'Location', cell: a => esc(a.location) },
      { title: 'Criticality', cell: a => badge(a.criticality) }, { title: 'Status', cell: a => badge(a.status) },
    ], data.items, { empty: 'No assets match. Add your first machine to start.', rowLink: a => `#/assets/${a.id}` })}
    ${pager(data, 'assets-page')}`;
  $('#filters').onsubmit = event => {
    event.preventDefault();
    location.hash = '#/assets?' + new URLSearchParams(new FormData(event.target));
  };
  actions['assets-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/assets?' + query; };
  actions['export-assets'] = () => exportExcel('/assets/export', {}, 'assets.xlsx');
  actions['add-asset'] = async () => {
    const created = await formDialog({
      title: 'Add asset', submitLabel: 'Add asset',
      fields: [{ name: 'asset_code', label: 'Asset code', required: true, hint: 'Unique in your factory, e.g. CNC-01. It cannot be changed later.' }, ...ASSET_FIELDS({})],
      submit: values => api('/assets', { method: 'POST', body: values }),
    });
    if (created) location.hash = `#/assets/${created.id}`;
  };
};

async function assetDetail(id) {
  const a = await api(`/assets/${id}`);
  const s = a.breakdown_summary;
  const records = list => list.map(r => `<a href="#/breakdowns?asset_id=${esc(a.id)}">${esc(r.record_no)}</a>`).join(', ');
  const repeats = (title, groups) => groups.length ? `<h3>${title}</h3><ul>${groups.map(g =>
    `<li><b>${esc(g.label)}</b> — ${g.count} times, ${g.downtime_minutes} min downtime · records ${records(g.records)}</li>`).join('')}</ul>` : '';
  const gaps = s && s.data_gaps;
  page().innerHTML = `
    <div class="page-head"><div><a href="#/assets">← Assets</a><h1>${esc(a.asset_code)} — ${esc(a.name)}</h1></div>
      <div class="actions">
        ${can('chat.ask') ? `<a class="btn" href="#/chat?asset=${esc(a.id)}">Ask about this asset</a>` : ''}
        ${can('work_orders.draft') ? '<button class="btn primary" data-action="draft-wo">Draft work order</button>' : ''}
        ${can('assets.manage') ? '<button class="btn" data-action="edit-asset">Edit</button>' : ''}
        ${can('assets.manage') && a.status !== 'archived' ? '<button class="btn danger" data-action="archive-asset">Archive</button>' : ''}
      </div></div>
    <div class="two-col">
      <div class="card"><h2>${fa('circle-info')}Details</h2><dl class="kv">
        <dt>Status</dt><dd>${badge(a.status)}</dd><dt>Criticality</dt><dd>${badge(a.criticality)}</dd>
        <dt>Type</dt><dd>${shown(a.asset_type)}</dd><dt>Manufacturer</dt><dd>${shown(a.manufacturer)}</dd>
        <dt>Model</dt><dd>${shown(a.model)}</dd><dt>Serial number</dt><dd>${shown(a.serial_number)}</dd>
        <dt>Location</dt><dd>${shown(a.location)}</dd></dl></div>
      ${s ? `<div class="card"><h2>${fa('chart-simple')}Breakdown history: recorded facts</h2>
        ${s.total_records ? `<dl class="kv">
          <dt>Records</dt><dd>${s.total_records} (${s.open_records} unresolved)</dd>
          <dt>Recorded downtime</dt><dd>${s.total_downtime_minutes} minutes</dd>
          <dt>Period</dt><dd>${day(s.first_reported_at)} – ${day(s.last_reported_at)}</dd></dl>
          ${repeats('Repeated error codes', s.repeat_error_codes)}${repeats('Repeated symptoms', s.repeat_symptoms)}${repeats('Repeated root causes', s.repeat_root_causes)}
          ${!s.repeat_error_codes.length && !s.repeat_symptoms.length && !s.repeat_root_causes.length ? '<p class="muted">No issue has been recorded more than once.</p>' : ''}
          ${gaps.root_cause_not_recorded.length || gaps.downtime_not_recorded.length ? `<div class="notice warn">Missing information:
            ${gaps.root_cause_not_recorded.length ? `root cause not recorded in ${gaps.root_cause_not_recorded.length} record(s) (${records(gaps.root_cause_not_recorded)}). ` : ''}
            ${gaps.downtime_not_recorded.length ? `Downtime not recorded in ${gaps.downtime_not_recorded.length} record(s) (${records(gaps.downtime_not_recorded)}).` : ''}</div>` : ''}
          <p class="hint">Counted directly from the breakdown records. No AI interpretation is involved here.</p>`
        : '<div class="empty">No breakdowns recorded for this asset.</div>'}
      </div>` : ''}
    </div>
    ${a.documents ? `<div class="card"><h2>${fa('book-open')}Linked documents</h2>${table([
      { title: 'File', cell: d => `<a href="#" data-action="open-doc" data-id="${esc(d.id)}">${esc(d.filename)}</a>` },
      { title: 'Type', cell: d => label(d.doc_type) }, { title: 'Status', cell: d => badge(d.status) },
    ], a.documents, { empty: 'No document is linked to this asset. Upload its manual or SOP under Documents.' })}</div>` : ''}
    ${a.recent_breakdowns ? `<div class="card"><h2>${fa('triangle-exclamation')}Recent breakdowns</h2>${breakdownTable(a.recent_breakdowns, false)}</div>` : ''}
    ${a.work_orders ? `<div class="card"><h2>${fa('clipboard-list')}Work orders</h2>${workOrderTable(a.work_orders)}</div>` : ''}`;
  actions['edit-asset'] = async () => {
    if (await formDialog({ title: `Edit ${a.asset_code}`, fields: ASSET_FIELDS(a), submit: values => api(`/assets/${id}`, { method: 'PATCH', body: values }) })) route();
  };
  actions['archive-asset'] = async () => {
    if (await confirmDialog(`Archive ${a.asset_code}?`, 'The asset leaves the everyday list. Its documents, breakdowns and work orders are kept.', 'Archive', 'danger')) {
      if (await attempt(() => api(`/assets/${id}/archive`, { method: 'POST' }), 'Asset archived')) location.hash = '#/assets';
    }
  };
  actions['draft-wo'] = () => newWorkOrder(a.id);
}

pages.documents = async (_, query) => {
  const params = { status: query.get('status') || '', page: query.get('page') || 1 };
  const [data, assets] = await Promise.all([api('/documents', { params }), assetOptions()]);
  const names = Object.fromEntries(assets.map(([id, text]) => [id, text.split(' — ')[0]]));
  page().innerHTML = `
    <div class="page-head"><h1>Document library</h1>
      ${can('documents.manage') ? '<button class="btn primary" data-action="upload">Upload document</button>' : ''}</div>
    <form class="filters" id="filters"><label>Status<select name="status">${['', 'ready', 'queued', 'processing', 'failed'].map(v => `<option value="${v}" ${v === params.status ? 'selected' : ''}>${v ? label(v) : 'All'}</option>`).join('')}</select></label>
      <button class="btn" type="submit">Apply</button></form>
    ${table([
      { title: 'File', cell: d => `<a href="#" data-action="open-doc" data-id="${esc(d.id)}">${esc(d.filename)}</a><div class="hint">${(d.size_bytes / 1024).toFixed(0)} KB · uploaded ${when(d.created_at)} by ${esc(d.uploaded_by_name)}</div>` },
      { title: 'Type', cell: d => label(d.doc_type) },
      { title: 'Assets', cell: d => d.asset_ids.length ? d.asset_ids.map(i => esc(names[i] || 'archived asset')).join(', ') : '<span class="muted">General</span>' },
      { title: 'Status', cell: d => `${badge(d.status)}${d.error ? `<div class="hint" style="color:var(--bad)">${esc(d.error)}</div>` : ''}` },
      { title: 'Indexed', num: true, cell: d => d.status === 'ready' ? `${d.chunk_count} sections${d.page_count ? ` · ${d.page_count} pages` : ''}` : '—' },
      { title: '', cell: d => can('documents.manage') ? `<div class="actions">
          ${['failed', 'ready'].includes(d.status) ? `<button class="btn small" data-action="reprocess" data-id="${esc(d.id)}">Reprocess</button>` : ''}
          <button class="btn small danger" data-action="delete-doc" data-id="${esc(d.id)}" data-name="${esc(d.filename)}">Delete</button></div>` : '' },
    ], data.items, { empty: 'No documents yet. Upload a machine manual, SOP or parts list (PDF, DOCX, PPTX, XLSX, CSV, TXT).' })}
    ${pager(data, 'docs-page')}`;
  $('#filters').onsubmit = event => { event.preventDefault(); location.hash = '#/documents?' + new URLSearchParams(new FormData(event.target)); };
  actions['docs-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/documents?' + query; };
  actions.upload = async () => {
    const done = await formDialog({
      title: 'Upload document', submitLabel: 'Upload',
      note: 'Processing runs in the background; the status column shows when the document is ready to search.',
      fields: [
        { name: 'file', label: 'File', type: 'file', required: true, accept: '.pdf,.docx,.pptx,.xlsx,.csv,.txt,.md', hint: 'PDF, DOCX, PPTX, XLSX, CSV, TXT or MD. An Excel sheet needs its column names in the first row. Scanned pages are not supported yet.' },
        { name: 'doc_type', label: 'Document type', type: 'select', options: [['manual', 'Machine manual'], ['sop', 'SOP / procedure'], ['spare_parts', 'Spare-parts list'], ['other', 'Other']], value: 'manual' },
        { name: 'asset_ids', label: 'Applies to assets', type: 'select', multiple: true, options: assets, hint: 'Hold Ctrl to select several. Leave empty for a general document.' },
      ],
      submit: values => {
        const form = new FormData();
        form.append('file', values.file);
        form.append('doc_type', values.doc_type);
        form.append('asset_ids', values.asset_ids.join(','));
        return api('/documents', { method: 'POST', form });
      },
    });
    if (done) { toast('Uploaded. Processing started.'); route(); }
  };
  actions.reprocess = async el => { if (await attempt(() => api(`/documents/${el.dataset.id}/reprocess`, { method: 'POST' }), 'Processing started')) route(); };
  actions['delete-doc'] = async el => {
    if (await confirmDialog(`Delete ${el.dataset.name}?`, 'The file and its search index entries are removed. Answers can no longer cite it.', 'Delete', 'danger')) {
      if (await attempt(() => api(`/documents/${el.dataset.id}`, { method: 'DELETE' }), 'Document deleted') !== undefined) route();
    }
  };
  // While something is still processing, refresh until it settles
  if (data.items.some(d => ['queued', 'processing'].includes(d.status))) pollTimer = setTimeout(route, 2500);
};

function breakdownTable(rows, showAsset = true) {
  return table([
    { title: 'Record', cell: b => `<b>${esc(b.record_no)}</b>` },
    ...(showAsset ? [{ title: 'Asset', cell: b => `<a href="#/assets/${esc(b.asset_id)}">${esc(b.asset_code)}</a>` }] : []),
    { title: 'Reported', cell: b => when(b.reported_at) },
    { title: 'Symptoms', cell: b => `${esc(b.symptoms)}${b.error_code ? ` <span class="badge">${esc(b.error_code)}</span>` : ''}` },
    { title: 'Downtime (min)', num: true, cell: b => shown(b.downtime_minutes) },
    { title: 'Root cause', cell: b => shown(b.root_cause) },
    { title: 'Corrective action', cell: b => shown(b.corrective_action) },
    { title: 'Status', cell: b => badge(b.resolution_status) },
    ...(can('breakdowns.report') ? [{ title: '', cell: b => `<button class="btn small" data-action="edit-breakdown" data-id="${esc(b.id)}">Update</button>` }] : []),
  ], rows, { empty: 'No breakdown records match.' });
}

const BREAKDOWN_EDIT_FIELDS = b => [
  { name: 'error_code', label: 'Error code', value: b.error_code },
  { name: 'downtime_minutes', label: 'Downtime (minutes)', type: 'number', min: 0, value: b.downtime_minutes },
  { name: 'root_cause', label: 'Root cause', type: 'textarea', rows: 2, value: b.root_cause, hint: 'Leave empty if it is not known. It will be shown as “not recorded”.' },
  { name: 'corrective_action', label: 'Corrective action', type: 'textarea', rows: 2, value: b.corrective_action },
  { name: 'parts_used', label: 'Parts used', value: b.parts_used },
  { name: 'resolution_status', label: 'Status', type: 'select', options: ['open', 'in_progress', 'resolved'], value: b.resolution_status || 'open' },
];

actions['edit-breakdown'] = async el => {
  const found = await attempt(() => api('/breakdowns', { params: { page_size: 200 } }));
  const record = found && found.items.find(b => b.id === el.dataset.id);
  if (!record) return;
  if (await formDialog({
    title: `Update ${record.record_no}`, fields: [{ name: 'symptoms', label: 'Symptoms', type: 'textarea', rows: 2, required: true, value: record.symptoms }, ...BREAKDOWN_EDIT_FIELDS(record)],
    submit: values => api(`/breakdowns/${record.id}`, { method: 'PATCH', body: values }),
  })) route();
};

pages.breakdowns = async (_, query) => {
  const assets = await assetOptions();
  const params = Object.fromEntries(['asset_id', 'status', 'q', 'error_code', 'date_from', 'date_to'].map(k => [k, query.get(k) || '']));
  if (query.get('asset')) params.q = query.get('asset');
  const data = await api('/breakdowns', { params: { ...params, page: query.get('page') || 1, date_to: params.date_to && params.date_to + 'T23:59:59' } });
  page().innerHTML = `
    <div class="page-head"><h1>Breakdown history</h1><div class="actions">
      <button class="btn" data-action="export-breakdowns">Export Excel</button>
      ${can('breakdowns.import') ? '<button class="btn" data-action="import">Import CSV / XLSX</button>' : ''}
      ${can('breakdowns.report') ? '<button class="btn primary" data-action="add-breakdown">Report breakdown</button>' : ''}</div></div>
    <form class="filters" id="filters">
      <label>Asset<select name="asset_id"><option value="">All</option>${assets.map(([id, text]) => `<option value="${esc(id)}" ${id === params.asset_id ? 'selected' : ''}>${esc(text)}</option>`).join('')}</select></label>
      <label>Status<select name="status">${['', 'open', 'in_progress', 'resolved'].map(v => `<option value="${v}" ${v === params.status ? 'selected' : ''}>${v ? label(v) : 'All'}</option>`).join('')}</select></label>
      <label>Words<input name="q" value="${esc(params.q)}" placeholder="Symptom, cause…"></label>
      <label>Error code<input name="error_code" value="${esc(params.error_code)}"></label>
      <label>From<input type="date" name="date_from" value="${esc(params.date_from)}"></label>
      <label>To<input type="date" name="date_to" value="${esc(params.date_to)}"></label>
      <button class="btn" type="submit">Apply</button><a class="btn" href="#/breakdowns">Clear</a>
    </form>
    ${breakdownTable(data.items)}${pager(data, 'bd-page')}`;
  $('#filters').onsubmit = event => { event.preventDefault(); location.hash = '#/breakdowns?' + new URLSearchParams(new FormData(event.target)); };
  actions['bd-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/breakdowns?' + query; };
  actions['add-breakdown'] = async () => {
    if (!assets.length) return toast('Add an asset first.', true);
    const local = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    if (await formDialog({
      title: 'Report breakdown', submitLabel: 'Save record',
      fields: [
        { name: 'asset_id', label: 'Asset', type: 'select', options: assets, value: params.asset_id || assets[0][0], required: true },
        { name: 'reported_at', label: 'Reported at', type: 'datetime-local', value: local, required: true },
        { name: 'symptoms', label: 'Symptoms', type: 'textarea', rows: 2, required: true },
        ...BREAKDOWN_EDIT_FIELDS({}),
      ],
      submit: values => api('/breakdowns', { method: 'POST', body: { ...values, reported_at: new Date(values.reported_at).toISOString() } }),
    })) route();
  };
  actions['export-breakdowns'] = () => exportExcel(
    '/breakdowns/export', { ...params, date_to: params.date_to && params.date_to + 'T23:59:59' }, 'breakdowns.xlsx');
  actions.import = async () => {
    let report = null;
    const done = await formDialog({
      title: 'Import breakdown records', submitLabel: 'Check and import',
      note: 'Required columns: asset_code, reported_at, symptoms. Valid rows are imported; every rejected row is listed with its reason. Rows already imported (same source_record_id) are skipped.',
      fields: [{ name: 'file', label: 'CSV or XLSX file', type: 'file', required: true, accept: '.csv,.xlsx' }],
      submit: async values => {
        const form = new FormData();
        form.append('file', values.file);
        report = await api('/breakdowns/import', { method: 'POST', form });
        return report;
      },
    });
    if (!done) return;
    await formDialog({
      title: 'Import result', submitLabel: 'Close',
      note: `${report.imported} imported, ${report.skipped_duplicates} already present, ${report.rejected} rejected out of ${report.total_rows} rows.`
        + (report.errors.length ? ' Rejected rows: ' + report.errors.slice(0, 15).map(e => `row ${e.row}: ${e.error}`).join(' · ') : ''),
      submit: async () => true,
    });
    route();
  };
};

function workOrderTable(rows) {
  return table([
    { title: 'No.', cell: w => `<b>${esc(w.order_no)}</b>` }, { title: 'Title', cell: w => esc(w.title) },
    { title: 'Asset', cell: w => esc(w.asset_code) }, { title: 'Priority', cell: w => badge(w.priority) },
    { title: 'Status', cell: w => badge(w.status) }, { title: 'Created', cell: w => `${when(w.created_at)}<div class="hint">${esc(w.created_by_name)}</div>` },
  ], rows, { empty: 'No work orders here.', rowLink: w => `#/work-orders/${w.id}` });
}

async function newWorkOrder(assetId) {
  const assets = await assetOptions();
  if (!assets.length) return toast('Add an asset first.', true);
  const created = await formDialog({
    title: 'Draft a work order', submitLabel: 'Create draft',
    note: 'With “Generate from records”, the draft is built from this asset’s SOPs and breakdown history and shows its sources. It is only a draft: nothing happens until someone with approval access approves it.',
    fields: [
      { name: 'asset_id', label: 'Asset', type: 'select', options: assets, value: assetId || assets[0][0], required: true },
      { name: 'problem', label: 'Problem / job description', type: 'textarea', rows: 3, required: true, maxlength: 2000 },
      { name: 'mode', label: 'How', type: 'select', options: [['generate', 'Generate from records (AI draft with sources)'], ['manual', 'Write it myself (empty draft)']], value: 'generate' },
    ],
    submit: values => values.mode === 'generate'
      ? api('/work-orders/generate', { method: 'POST', body: { asset_id: values.asset_id, problem: values.problem } })
      : api('/work-orders', { method: 'POST', body: { asset_id: values.asset_id, title: values.problem.slice(0, 100), description: values.problem } }),
  });
  if (created) location.hash = `#/work-orders/${created.id}`;
}

pages['work-orders'] = async (id, query) => {
  if (id) return workOrderDetail(id);
  const status = query.get('status') || '';
  const data = await api('/work-orders', { params: { status, page: query.get('page') || 1 } });
  const tabs = [['', 'All'], ['draft', 'Drafts'], ['pending_approval', 'Approval queue'], ['approved', 'Approved'], ['in_progress', 'In progress'], ['completed', 'Completed'], ['rejected', 'Rejected']];
  page().innerHTML = `
    <div class="page-head"><h1>Work orders</h1><div class="actions">
      <button class="btn" data-action="export-wo">Export Excel</button>
      ${can('work_orders.draft') ? '<button class="btn primary" data-action="new-wo">Draft work order</button>' : ''}</div></div>
    <div class="tabs">${tabs.map(([v, t]) => `<a class="tab ${v === status ? 'active' : ''}" href="#/work-orders${v ? '?status=' + v : ''}">${t}</a>`).join('')}</div>
    ${workOrderTable(data.items)}${pager(data, 'wo-page')}`;
  actions['export-wo'] = () => exportExcel('/work-orders/export', { status }, 'work_orders.xlsx');
  actions['wo-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/work-orders?' + query; };
  actions['new-wo'] = () => newWorkOrder();
};

async function workOrderDetail(id) {
  const w = await api(`/work-orders/${id}`);
  const flags = item => `<span class="flags">
    ${item.sources.length ? `<span class="cite-ref">[${item.sources.join(', ')}]</span>` : ''}
    ${item.safety_review ? '<span class="badge bad">Safety: qualified review needed</span>' : ''}
    ${item.unsupported ? '<span class="badge warn">No source in the records</span>' : ''}</span>`;
  page().innerHTML = `
    <div class="page-head"><div><a href="#/work-orders">← Work orders</a><h1>${esc(w.order_no)} — ${esc(w.title)}</h1></div>
      <div class="actions">${w.can_edit ? '<button class="btn" data-action="edit-wo">Edit draft</button>' : ''}
        ${w.allowed_transitions.map(to => `<button class="btn ${['approved', 'pending_approval', 'in_progress', 'completed'].includes(to) ? 'primary' : to === 'draft' ? '' : 'danger'}" data-action="move" data-to="${to}">${MOVE_LABEL[to]}</button>`).join('')}</div></div>
    ${w.status === 'draft' ? `<div class="notice">This is a draft${w.generated ? ' generated from your records' : ''}. Nothing is carried out until it is submitted and approved by someone with approval access${w.generated ? '; check every step against its source first' : ''}.</div>` : ''}
    <div class="two-col">
      <div class="card"><h2>${fa('circle-info')}Details</h2><dl class="kv">
        <dt>Status</dt><dd>${badge(w.status)}</dd><dt>Priority</dt><dd>${badge(w.priority)}</dd>
        <dt>Asset</dt><dd><a href="#/assets/${esc(w.asset_id)}">${esc(w.asset_code)}</a></dd>
        <dt>Created</dt><dd>${when(w.created_at)} by ${esc(w.created_by_name)}</dd>
        <dt>Approved</dt><dd>${w.approved_at ? `${when(w.approved_at)} by ${esc(w.approved_by_name)}` : '<span class="muted">not approved</span>'}</dd>
        <dt>Work started</dt><dd>${when(w.executed_at)}</dd><dt>Completed</dt><dd>${when(w.completed_at)}</dd></dl>
        <h3 style="margin-top:14px">Description</h3><div style="white-space:pre-wrap">${withRefs(w.description) || '<span class="muted">No description.</span>'}</div></div>
      <div class="card"><h2>${fa('clock-rotate-left')}History</h2><ul class="timeline">${w.history.map(h =>
        `<li>${badge(h.to)} ${when(h.at)} · ${esc(h.by_name)}${h.comment ? `<div class="hint">“${esc(h.comment)}”</div>` : ''}</li>`).join('')}</ul></div>
    </div>
    <div class="card"><h2>${fa('list-check')}Proposed checklist</h2>
      ${w.proposed_checklist.length ? `<ol class="checklist">${w.proposed_checklist.map(i => `<li>${esc(i.step)}${flags(i)}</li>`).join('')}</ol>` : '<div class="empty">No steps yet. Edit the draft to add them.</div>'}</div>
    <div class="card"><h2>${fa('magnifying-glass')}Evidence used</h2>${w.source_references.length ? sourceList(w.source_references).replace('class="sources"', 'class="sources" style="border:0;margin:0;padding:0"') : '<div class="empty">This work order cites no documents or records.</div>'}</div>`;
  actions['edit-wo'] = async () => {
    const sources = Object.fromEntries(w.proposed_checklist.map(i => [i.step, i.sources]));
    if (await formDialog({
      title: `Edit ${w.order_no}`,
      fields: [
        { name: 'title', label: 'Title', required: true, value: w.title, minlength: 3 },
        { name: 'priority', label: 'Priority', type: 'select', options: ['low', 'medium', 'high', 'critical'], value: w.priority },
        { name: 'description', label: 'Description', type: 'textarea', rows: 5, value: w.description },
        { name: 'checklist', label: 'Checklist', type: 'textarea', rows: 8, value: w.proposed_checklist.map(i => i.step).join('\n'), hint: 'One step per line. A step you change or add is marked “No source in the records”.' },
      ],
      submit: values => api(`/work-orders/${id}`, { method: 'PATCH', body: {
        title: values.title, priority: values.priority, description: values.description,
        checklist: values.checklist.split('\n').map(s => s.trim()).filter(Boolean).map(step => ({ step, sources: sources[step] || [] })),
      } }),
    })) route();
  };
  actions.move = async el => {
    const to = el.dataset.to;
    if (await formDialog({
      title: `${MOVE_LABEL[to]}: ${w.order_no}`, submitLabel: MOVE_LABEL[to],
      note: to === 'approved' ? 'By approving, you confirm you reviewed the checklist, including every step flagged for safety or without a source.' : '',
      fields: [{ name: 'comment', label: to === 'rejected' ? 'Reason' : 'Comment (optional)', type: 'textarea', rows: 2, required: to === 'rejected', maxlength: 1000 }],
      submit: values => api(`/work-orders/${id}/transition`, { method: 'POST', body: { to, comment: values.comment } }),
    })) route();
  };
}

const DECISIONS = [
  ['governs', 'One document governs'], ['outdated', 'One document is outdated'],
  ['both_apply', 'Both apply, under different conditions'], ['false_alarm', 'Not a real conflict'],
];

pages.conflicts = async (_, query) => {
  const params = { status: query.get('status') ?? 'open', kind: query.get('kind') || '', page: query.get('page') || 1 };
  const data = await api('/conflicts', { params });
  const decisionText = r => `${esc(Object.fromEntries(DECISIONS)[r.decision] || r.decision)}${r.document_name ? ` (${esc(r.document_name)})` : ''}`;
  page().innerHTML = `
    <div class="page-head"><h1>Conflicts between documents</h1></div>
    <div class="notice">Found when a question was asked and two of your documents gave different values for the same instruction.
      The assistant never picks one. A person with access to close conflicts records which applies; everyone who sees this page sees the decision.
      A decision is reopened when one of the documents changes.</div>
    <form class="filters" id="filters">
      <label>Status<select name="status">${[['open', 'Open'], ['resolved', 'Resolved'], ['', 'All']].map(([v, t]) => `<option value="${v}" ${v === params.status ? 'selected' : ''}>${t}</option>`).join('')}</select></label>
      <label>Kind<select name="kind">${[['', 'All'], ['conflict', 'Conflict'], ['needs_review', 'Needs review']].map(([v, t]) => `<option value="${v}" ${v === params.kind ? 'selected' : ''}>${t}</option>`).join('')}</select></label>
      <button class="btn" type="submit">Apply</button></form>
    ${data.items.length ? data.items.map(c => `
      <div class="card">
        <h2>${fa('code-compare')}${esc(c.topic || 'Instruction')} ${badge(c.kind)} ${badge(c.status)}</h2>
        ${c.claims.map(s => `<div class="source"><span><b>${esc(s.value)}</b> ·
            <a href="#" data-action="open-doc" data-id="${esc(s.document_id)}" data-page="${esc(s.page || '')}">${esc(s.filename)}</a>${s.revision ? ` · revision ${esc(s.revision)}` : ''}</span>
          <span class="excerpt">${esc(s.sentence)}</span></div>`).join('')}
        ${(c.differences || []).length ? `<p class="hint">Differences in conditions: ${esc(c.differences.join('; '))}.</p>` : ''}
        ${(c.notes || []).map(n => `<p class="hint">${esc(n)}</p>`).join('')}
        ${c.resolution ? `<p><b>Decision:</b> ${decisionText(c.resolution)} · ${esc(c.resolution.resolved_by_name)} · ${when(c.resolution.resolved_at)}<br>${esc(c.resolution.note)}</p>` : ''}
        <div class="actions"><span class="hint">Seen ${c.times_seen} time${c.times_seen === 1 ? '' : 's'}, last ${when(c.last_seen_at)}${(c.history || []).length ? ` · ${c.history.length} earlier decision${c.history.length === 1 ? '' : 's'}` : ''}</span>
          ${c.status === 'open' && can('conflicts.resolve') ? `<button class="btn primary small" data-action="resolve-conflict" data-id="${esc(c.id)}">Record a decision</button>` : ''}</div>
      </div>`).join('') : '<div class="empty">No conflicts match.</div>'}${pager(data, 'conflict-page')}`;
  $('#filters').onsubmit = event => { event.preventDefault(); location.hash = '#/conflicts?' + new URLSearchParams(new FormData(event.target)); };
  actions['conflict-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/conflicts?' + query; };
  actions['resolve-conflict'] = async el => {
    const conflict = data.items.find(c => c.id === el.dataset.id);
    const documents = [...new Map(conflict.claims.map(s => [s.document_id, `${s.filename} (${s.value})`]))];
    if (await formDialog({
      title: 'Record a decision', submitLabel: 'Record decision',
      note: 'You confirm that you checked the approved, current procedure. The decision is shown to everyone who asks about this and is written to the audit history.',
      fields: [
        { name: 'decision', label: 'Decision', type: 'select', options: DECISIONS, value: 'governs' },
        { name: 'document_id', label: 'Document the decision is about', type: 'select', options: [['', 'Not about one document'], ...documents], value: '' },
        { name: 'note', label: 'Reason', type: 'textarea', rows: 3, required: true, maxlength: 1000, hint: 'At least 10 characters: what you checked and why.' },
      ],
      submit: values => {
        const about = ['governs', 'outdated'].includes(values.decision);
        if (about && !values.document_id) throw new Error('Choose the document this decision is about.');
        if (values.note.length < 10) throw new Error('Give a reason of at least 10 characters.');
        return api(`/conflicts/${conflict.id}/resolve`, { method: 'POST', body: { decision: values.decision, document_id: about ? values.document_id : null, note: values.note } });
      },
    })) route();
  };
};

pages.audit = async (_, query) => {
  const params = { resource_type: query.get('resource_type') || '', result: query.get('result') || '', page: query.get('page') || 1 };
  const data = await api('/audit', { params });
  page().innerHTML = `
    <div class="page-head"><h1>Audit history</h1></div>
    <form class="filters" id="filters">
      <label>Record type<select name="resource_type">${['', 'work_order', 'document', 'conflict', 'asset', 'breakdown', 'user', 'organization', 'payment'].map(v => `<option value="${v}" ${v === params.resource_type ? 'selected' : ''}>${v ? label(v) : 'All'}</option>`).join('')}</select></label>
      <label>Result<select name="result">${['', 'success', 'denied', 'failed'].map(v => `<option value="${v}" ${v === params.result ? 'selected' : ''}>${v ? label(v) : 'All'}</option>`).join('')}</select></label>
      <button class="btn" type="submit">Apply</button></form>
    ${table([
      { title: 'When', cell: e => when(e.created_at) }, { title: 'Who', cell: e => esc(e.actor_name) },
      { title: 'Action', cell: e => esc(e.action) }, { title: 'Detail', cell: e => esc(e.detail) },
      { title: 'Result', cell: e => badge(e.result) }, { title: 'Request', cell: e => `<span class="muted">${esc(e.request_id.slice(0, 8))}</span>` },
    ], data.items, { empty: 'No audit events match.' })}${pager(data, 'audit-page')}`;
  $('#filters').onsubmit = event => { event.preventDefault(); location.hash = '#/audit?' + new URLSearchParams(new FormData(event.target)); };
  actions['audit-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/audit?' + query; };
};

pages.users = async () => {
  const [data, catalogue] = await Promise.all([api('/users'), api('/permissions')]);
  const roleOptions = ROLES.map(r => [r, ROLE_NAMES[r]]);
  const groups = [...new Set(catalogue.permissions.map(p => p.group))];
  const access = u => u.role === 'admin' ? 'Everything' : u.custom_permissions
    ? `<b>Custom</b> · ${u.permissions.length} of ${catalogue.permissions.length}` : 'Standard for the role';
  page().innerHTML = `
    <div class="page-head"><h1>Users</h1><button class="btn primary" data-action="add-user">Add user</button></div>
    <div class="card logo-card"><h2>${fa('image')}Company logo</h2>
      <div class="logo-row">${orgMark('logo-card-mark')}
        <div><p class="hint">Shown in the header and on the dashboard for everyone in ${esc(me.organization_name)}. PNG, JPG or WebP, up to 512 KB.</p>
        <div class="actions"><button class="btn small" data-action="logo-change">${me.organization_logo_url ? 'Change logo' : 'Upload logo'}</button>
          ${me.organization_logo_url ? '<button class="btn small danger" data-action="logo-remove">Remove</button>' : ''}</div></div></div></div>
    <div class="notice">A role gives a standard set of access. Viewer: read and ask. Technician: also report breakdowns, draft work orders and carry out approved ones.
      Maintenance manager: also manage assets and documents, import records, approve work orders and close conflicts. Administrator: everything, manages users, and may approve a work order they wrote themselves.
      With <b>Access</b> you choose for one user which sections are visible and what that user may do, for example who may approve work orders.</div>
    ${table([
      { title: 'Name', cell: u => esc(u.name) }, { title: 'Email', cell: u => esc(u.email) },
      { title: 'Role', cell: u => esc(ROLE_NAMES[u.role]) }, { title: 'Access', cell: access },
      { title: 'Status', cell: u => badge(u.is_active ? 'active' : 'inactive') },
      { title: '', cell: u => u.id === me.id ? '<span class="muted" title="Your own account">Admin</span>' : `<div class="actions">
          <button class="btn small" data-action="role" data-id="${esc(u.id)}">Change role</button>
          ${u.role === 'admin' ? '' : `<button class="btn small" data-action="access" data-id="${esc(u.id)}">Access</button>`}
          <button class="btn small ${u.is_active ? 'danger' : ''}" data-action="toggle-user" data-id="${esc(u.id)}" data-active="${u.is_active}">${u.is_active ? 'Deactivate' : 'Activate'}</button></div>` },
    ], data.items)}`;
  const picked = el => data.items.find(u => u.id === el.dataset.id);
  actions['logo-change'] = async () => {
    const result = await formDialog({
      title: 'Company logo', submitLabel: 'Upload',
      fields: [{ name: 'file', label: 'Picture', type: 'file', accept: 'image/png,image/jpeg,image/webp', required: true, hint: 'PNG, JPG or WebP, up to 512 KB.' }],
      submit: async values => {
        const form = new FormData();
        form.append('file', values.file);
        return api('/organization/logo', { method: 'PUT', form });
      },
    });
    if (!result) return;
    me.organization_logo_url = result.logo_url;
    showLogos();
    toast('Logo saved');
    route();
  };
  actions['logo-remove'] = async () => {
    if (!await confirmDialog('Remove the company logo?', 'The header and dashboard show the first letter of the company name instead.', 'Remove', 'danger')) return;
    if (await attempt(() => api('/organization/logo', { method: 'DELETE' }).then(() => true), 'Logo removed')) {
      me.organization_logo_url = null;
      showLogos();
      route();
    }
  };
  actions['add-user'] = async () => {
    if (await formDialog({
      title: 'Add user', submitLabel: 'Add user',
      note: 'The user starts with the standard access of the role. Use “Access” afterwards to change it for this user.',
      fields: [
        { name: 'name', label: 'Name', required: true, minlength: 2 }, { name: 'email', label: 'Email', type: 'email', required: true },
        { name: 'password', label: 'Initial password', type: 'password', required: true, minlength: 8, hint: 'At least 8 characters. Give it to the user personally.' },
        { name: 'role', label: 'Role', type: 'select', options: roleOptions, value: 'technician' },
      ],
      submit: values => api('/users', { method: 'POST', body: values }),
    })) route();
  };
  actions.role = async el => {
    const u = picked(el);
    if (await formDialog({
      title: `Role of ${u.name}`, fields: [{ name: 'role', label: 'Role', type: 'select', options: roleOptions, value: u.role }],
      note: u.custom_permissions ? 'This user has custom access. Changing the role replaces it with the standard access of the new role.' : '',
      submit: values => api(`/users/${u.id}`, { method: 'PATCH', body: values }),
    })) route();
  };
  actions.access = async el => {
    const u = picked(el);
    const standard = catalogue.role_defaults[u.role];
    if (await formDialog({
      title: `Access of ${u.name}`, submitLabel: 'Save access',
      note: `Tick what ${u.name} may see and do. “See …” decides whether the section appears in the menu; an action inside a section makes the section visible as well. `
        + `Ticking exactly the standard of the role (${ROLE_NAMES[u.role]}) keeps the user on that standard.`,
      fields: groups.map((group, i) => ({
        name: `group${i}`, label: group, type: 'checks', value: u.permissions,
        options: catalogue.permissions.filter(p => p.group === group).map(p => [p.key, p.label + (standard.includes(p.key) ? '' : ' (not in the role’s standard)')]),
      })),
      submit: values => {
        const chosen = Object.values(values).flat();
        const same = chosen.length === standard.length && chosen.every(key => standard.includes(key));
        return api(`/users/${u.id}`, { method: 'PATCH', body: { permissions: same ? null : chosen } });
      },
    })) route();
  };
  actions['toggle-user'] = async el => {
    const active = el.dataset.active !== 'true';
    if (await attempt(() => api(`/users/${el.dataset.id}`, { method: 'PATCH', body: { is_active: active } }), active ? 'User activated' : 'User deactivated and signed out')) route();
  };
};

// ---------- routing and session ----------

const sharedActions = { ...actions };
sharedActions['open-doc'] = el => openDocument(el.dataset.id, el.dataset.page);

function currentRoute() {
  const [path, search = ''] = location.hash.replace(/^#\/?/, '').split('?');
  const [name, id] = path.split('/');
  // Without an address, or with an unknown one: the first section this user may see
  const start = NAV.find(n => can(n[2])) || NAV[0];
  return { entry: NAV.find(n => n[0] === name) || start, id, search };
}

const OPENABLE = ['add-asset', 'add-breakdown', 'import'];

async function draw() {
  clearTimeout(pollTimer);
  charts.forEach(c => c.destroy());
  charts = [];
  const { entry, id, search } = currentRoute();
  actions = { ...sharedActions };
  if (!can(entry[2])) {
    page().innerHTML = '<div class="empty">You do not have access to this page. Ask an administrator if you need it.</div>';
    return;
  }
  try {
    await pages[entry[0]](id, new URLSearchParams(search));
    const heading = $('.page-head h1');
    if (heading && !heading.querySelector('i')) heading.insertAdjacentHTML('afterbegin', fa(entry[3]));
    // A link may open one of the page's own forms, e.g. the dashboard's "Add asset": #/assets?open=add-asset
    const open = new URLSearchParams(search).get('open');
    if (OPENABLE.includes(open) && actions[open]) {
      history.replaceState(null, '', location.hash.replace(/([?&])open=[^&]*&?/, '$1').replace(/[?&]$/, ''));
      actions[open]();
    }
  } catch (error) {
    if (token) page().innerHTML = `<div class="card"><h2>${fa('circle-exclamation')}This page could not be loaded</h2><p class="error">${esc(error.message)}</p><button class="btn" data-action="retry">Try again</button></div>`;
    actions.retry = route;
  }
}

// One page is drawn at a time, and only the address the user is on now: without this, a slow answer for a page
// they have already left is drawn over the page they went to
const drawLatest = latestOnly(draw);

function route() {
  const { entry } = currentRoute();
  document.querySelectorAll('#nav a').forEach(a => a.classList.toggle('active', a.dataset.page === entry[0]));
  return drawLatest();
}

document.addEventListener('click', event => {
  const trigger = event.target.closest('[data-action]');
  if (trigger && actions[trigger.dataset.action]) {
    event.preventDefault();
    actions[trigger.dataset.action](trigger);
    return;
  }
  const row = event.target.closest('tr[data-href]');
  if (row && !event.target.closest('a, button')) location.hash = row.dataset.href;
});
window.addEventListener('hashchange', () => { if (me) route(); });

// ---------- registration payment and company logo ----------

const rupees = amount => `₹${Number(amount).toLocaleString('en-IN')}`;

/** The company logo, or the first letter of its name when it has none. */
function orgMark(className) {
  return me.organization_logo_url
    ? `<img class="${className}" src="${esc(me.organization_logo_url)}" alt="${esc(me.organization_name)} logo">`
    : `<span class="${className} org-initial" aria-hidden="true">${esc(me.organization_name.trim().charAt(0).toUpperCase())}</span>`;
}

// Dashboard hero: a welcome beside the company's logo (its name is in the header, so it is not repeated here).
// The greeting rises letter by letter, a sun or moon badge shows the time of day, the card tilts towards the
// pointer with a light under it, and the quick actions are the sections this user may open.
function orgHero() {
  const hour = new Date().getHours();
  const [hello, sky, skyClass] = hour >= 5 && hour < 12 ? ['Good morning', 'sun', 'sky-morning']
    : hour >= 12 && hour < 17 ? ['Good afternoon', 'cloud-sun', 'sky-day'] : ['Good evening', 'moon', 'sky-night'];
  const greeting = `${hello}, ${me.name.trim().split(/\s+/)[0]}`;
  let i = 0;
  const words = greeting.split(' ')
    .map(word => `<span class="hero-word">${[...word].map(ch => `<span style="--i:${i++}">${esc(ch)}</span>`).join('')}</span>`)
    .join(' ');
  const actions = [
    ['chat.ask', '#/chat', 'comments', 'Ask'], ['documents.view', '#/documents', 'book-open', 'Documents'],
    ['breakdowns.view', '#/breakdowns', 'triangle-exclamation', 'Breakdowns'], ['work_orders.view', '#/work-orders', 'clipboard-list', 'Work orders'],
  ].filter(([permission]) => can(permission));
  const today = new Date().toLocaleDateString([], { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
  return `<section class="org-hero" id="org-hero">
    <span class="hero-light" aria-hidden="true"></span>
    <div class="hero-mark ${skyClass}"><span class="hero-ring" aria-hidden="true"></span>${orgMark('org-banner-logo')}<span class="hero-sky" aria-hidden="true">${fa(sky)}</span></div>
    <div class="hero-text">
      <div class="hero-hello"><i class="fa-solid fa-hand hero-wave" aria-hidden="true"></i>Welcome back</div>
      <h2 class="hero-name" aria-label="${esc(greeting)}"><span aria-hidden="true">${words}</span></h2>
      <div class="hero-meta">
        <span class="hero-chip">${fa('shield-halved')}${esc(ROLE_NAMES[me.role])}</span>
        <span class="hero-chip">${fa('calendar-day')}${esc(today)}</span>
      </div>
    </div>
    ${actions.length ? `<nav class="hero-actions" aria-label="Quick actions">${actions.map(([, href, icon, text], k) =>
      `<a href="${href}" style="--i:${k}">${fa(icon)}<span>${text}</span>${fa('arrow-right hero-go')}</a>`).join('')}</nav>` : ''}
  </section>`;
}

function heroMotion() {
  const hero = $('#org-hero');
  if (!hero || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  hero.addEventListener('pointermove', event => {
    const box = hero.getBoundingClientRect();
    const x = (event.clientX - box.left) / box.width;
    const y = (event.clientY - box.top) / box.height;
    hero.style.setProperty('--rx', `${((0.5 - y) * 5).toFixed(2)}deg`);
    hero.style.setProperty('--ry', `${((x - 0.5) * 6).toFixed(2)}deg`);
    hero.style.setProperty('--mx', `${(x * 100).toFixed(1)}%`);
    hero.style.setProperty('--my', `${(y * 100).toFixed(1)}%`);
  });
  hero.addEventListener('pointerleave', () => {
    hero.style.setProperty('--rx', '0deg');
    hero.style.setProperty('--ry', '0deg');
  });
}

function setImage(img, url) {
  img.hidden = !url;
  if (url) img.src = url;
  else img.removeAttribute('src');
}

// The header is a dark band: there the logo's own background is taken out and its marks are drawn in white, so a
// JPG on white, a PNG on transparent or a logo on a dark plate all sit on the header as if printed on it.
// A photograph has no marks to keep (busy corners, colour everywhere): it is shown as it is, framed.
async function headerLogo(url) {
  const img = await new Promise((resolve, reject) => {
    const picture = new Image();
    picture.onload = () => resolve(picture);
    picture.onerror = reject;
    picture.src = url;
  });
  const scale = Math.min(1, 160 / img.naturalHeight, 480 / img.naturalWidth);
  const w = Math.max(1, Math.round(img.naturalWidth * scale));
  const h = Math.max(1, Math.round(img.naturalHeight * scale));
  const canvas = Object.assign(document.createElement('canvas'), { width: w, height: h });
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  ctx.drawImage(img, 0, 0, w, h);
  const data = ctx.getImageData(0, 0, w, h);
  const px = data.data;
  const corners = [0, w - 1, (h - 1) * w, h * w - 1].map(i => px.slice(i * 4, i * 4 + 4));
  const clear = corners.every(c => c[3] < 40);
  const bg = [0, 1, 2].map(k => corners.reduce((sum, c) => sum + c[k], 0) / 4);
  const distance = (r, g, b) => Math.hypot(r - bg[0], g - bg[1], b - bg[2]);
  if (!clear && corners.some(c => distance(c[0], c[1], c[2]) > 60)) return { src: url, photo: true };
  let ink = 0, left = w, top = h, right = -1, bottom = -1;
  for (let i = 0; i < w * h; i++) {
    const p = i * 4;
    const alpha = px[p + 3] / 255;
    const mark = clear ? alpha : Math.min(1, distance(px[p], px[p + 1], px[p + 2]) / 120) * alpha;
    px[p] = px[p + 1] = px[p + 2] = 255;
    px[p + 3] = Math.round(mark * 255);
    if (mark > 0.15) {
      ink++;
      const x = i % w, y = (i / w) | 0;
      left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y);
    }
  }
  if (right < 0 || ink / (w * h) > 0.55) return { src: url, photo: true };
  ctx.putImageData(data, 0, 0);
  const pad = 2;
  const x0 = Math.max(0, left - pad), y0 = Math.max(0, top - pad);
  const out = Object.assign(document.createElement('canvas'), { width: Math.min(w, right + pad + 1) - x0, height: Math.min(h, bottom + pad + 1) - y0 });
  out.getContext('2d').drawImage(canvas, x0, y0, out.width, out.height, 0, 0, out.width, out.height);
  return { src: out.toDataURL('image/png'), photo: false };
}

function showLogos() {
  const url = me.organization_logo_url;
  const box = $('#hdr-logo');
  box.hidden = true; // shown once the white version is ready, never as a white box first
  setImage($('#hdr-logo img'), null);
  $('#hdr-logo img').alt = url ? `${me.organization_name} logo` : '';
  if (url) {
    headerLogo(url)
      .catch(() => ({ src: url, photo: true }))
      .then(({ src, photo }) => {
        if (me?.organization_logo_url !== url) return; // a newer logo or another user meanwhile
        box.classList.toggle('photo', photo);
        setImage($('#hdr-logo img'), src);
        box.hidden = false;
      });
  }
  $('#chip-icon').hidden = Boolean(url);
  setImage($('#chip-logo'), url);
  setImage($('#pay-logo'), url);
}

// Razorpay Checkout, loaded only when someone pays
let checkoutScript = null;
const loadCheckout = () => checkoutScript ||= new Promise((resolve, reject) => {
  const script = document.createElement('script');
  script.src = 'https://checkout.razorpay.com/v1/checkout.js';
  script.onload = resolve;
  script.onerror = () => {
    checkoutScript = null;
    script.remove();
    reject(new Error('Razorpay could not be loaded. Check the internet connection and try again.'));
  };
  document.head.append(script);
});

async function showPayment() {
  $('#auth').hidden = true;
  $('#app').hidden = true;
  $('#pay').hidden = false;
  $('#pay-org').textContent = me.organization_name;
  showLogos();
  await drawPayment();
}

async function enterApp(message) {
  me = await api('/auth/me');
  toast(message);
  showApp();
}

async function drawPayment() {
  if (!me) return;
  const body = $('#pay-body');
  let b;
  try {
    b = await api('/billing');
  } catch (error) {
    body.innerHTML = `<p class="error">${esc(error.message)}</p><button class="btn" id="pay-retry">Try again</button>`;
    $('#pay-retry').onclick = () => drawPayment();
    return;
  }
  if (b.status === 'active') return enterApp('Payment received. Your company is registered.');
  const failed = b.payments[0]?.error;
  body.innerHTML = `
    <h1>Pay ${rupees(b.fee)} to activate your company</h1>
    <p class="muted">Card, UPI, net banking or wallet, through Razorpay. Your company is active as soon as the payment goes through.</p>
    ${b.test_mode ? `<div class="pay-test">
      <div class="pay-test-head">${fa('flask')}Test payment: no real money</div>
      <ol><li>Press <b>Pay ${rupees(b.fee)}</b> and choose <b>UPI</b>.</li>
        <li>Enter the UPI ID <code>success@razorpay</code> and pay.</li></ol>
      <div class="muted">With net banking, press <b>Success</b> on Razorpay's test bank page.</div></div>` : ''}
    ${b.configured
      ? `<button class="btn primary pay-now" id="pay-now" type="button">${fa('lock')}Pay ${rupees(b.fee)}</button>
         ${failed ? `<div class="pay-failed">${fa('circle-exclamation')}<div><b>Your last payment did not go through.</b>
           <span>${esc(failed)}</span><span class="muted">Nothing was charged. Press Pay to try again.</span></div></div>` : ''}
         <p class="hint pay-secure">${fa('shield-halved')}Payments are handled by Razorpay. This application never sees card or bank details.</p>`
      : '<div class="notice">Payments are not set up on this server yet. Contact the platform owner.</div>'}`;
  const button = $('#pay-now');
  if (button) button.onclick = () => payNow(button);
}

async function payNow(button) {
  const idle = button.innerHTML;
  const busy = text => { button.disabled = true; button.innerHTML = `${fa('spinner fa-spin')}${text}`; };
  busy('Opening Razorpay…');
  try {
    await loadCheckout();
    const order = await api('/billing/order', { method: 'POST' });
    const checkout = new window.Razorpay({
      key: order.key_id, order_id: order.order_id, amount: order.amount, currency: order.currency,
      name: order.name, description: order.description, prefill: order.prefill, theme: { color: '#4f46e5' },
      handler: async ({ razorpay_order_id, razorpay_payment_id, razorpay_signature }) => {
        busy('Confirming the payment…');
        try {
          await api('/billing/verify', { method: 'POST', body: { razorpay_order_id, razorpay_payment_id, razorpay_signature } });
          await enterApp('Payment received. Your company is registered.');
        } catch (error) {
          toast(error.message, true);
          await drawPayment();
        }
      },
      // Closed without paying, or after paying but before reporting back: the server asks Razorpay again
      modal: { ondismiss: () => drawPayment() },
    });
    // Checkout stays open for another try; the server records the failure once Razorpay confirms it, and mails it
    checkout.on('payment.failed', response => {
      toast(response.error?.description || 'The payment did not go through. Try again.', true);
      const paymentId = response.error?.metadata?.payment_id;
      if (paymentId) api('/billing/failed', { method: 'POST', body: { razorpay_payment_id: paymentId } }).catch(() => {});
    });
    checkout.open();
    button.disabled = false;
    button.innerHTML = idle;
  } catch (error) {
    toast(error.message, true);
    button.disabled = false;
    button.innerHTML = idle;
  }
}

$('#pay-sign-out').onclick = async () => {
  await api('/auth/logout', { method: 'POST' }).catch(() => {});
  signOut();
};

pages.payments = async (_, query) => {
  const params = { status: query.get('status') || '', page: query.get('page') || 1 };
  const data = await api('/platform/payments', { params });
  page().innerHTML = `
    <div class="page-head"><h1>Payments</h1></div>
    <div class="notice">Registration fees of new companies, paid through Razorpay. A company becomes active by itself once Razorpay
      confirms its payment. Refunds and settlements are in the Razorpay Dashboard.</div>
    <form class="filters" id="filters"><label>Status<select name="status">${[['', 'All'], ['paid', 'Paid'], ['unpaid', 'Unpaid']]
      .map(([v, t]) => `<option value="${v}" ${v === params.status ? 'selected' : ''}>${t}</option>`).join('')}</select></label>
      <button class="btn" type="submit">Apply</button></form>
    ${table([
      { title: 'When', cell: p => when(p.paid_at || p.created_at) },
      { title: 'Company', cell: p => `${esc(p.organization_name)}<div class="muted">${esc(p.created_by_email)}</div>` },
      { title: 'Amount', num: true, cell: p => rupees(p.amount) },
      { title: 'Razorpay', cell: p => `${p.payment_id ? `<code>${esc(p.payment_id)}</code>` : ''}<div class="muted">${esc(p.order_id)}${p.method ? ` · ${esc(p.method)}` : ''}</div>` },
      { title: 'Status', cell: p => badge(p.status) + (p.test_mode ? ' <span class="badge">test</span>' : '') + (p.error ? `<div class="muted">${esc(p.error)}</div>` : '') },
    ], data.items, { empty: 'No payments here.' })}${pager(data, 'pay-page')}`;
  $('#filters').onsubmit = event => { event.preventDefault(); location.hash = '#/payments?' + new URLSearchParams(new FormData(event.target)); };
  actions['pay-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/payments?' + query; };
};

function showApp() {
  if (me.organization_status !== 'active') {
    showPayment();
    return;
  }
  $('#auth').hidden = true;
  $('#pay').hidden = true;
  $('#app').hidden = false;
  $('#org-name').textContent = me.organization_name;
  showLogos();
  $('#who-name').textContent = me.name;
  $('#who-role').textContent = ROLE_NAMES[me.role] + (me.custom_permissions ? ' · custom' : '');
  $('#who-avatar').textContent = me.name.trim().charAt(0);
  let section = '';
  $('#nav').innerHTML = NAV.filter(n => can(n[2])).map(([key, text, , icon, group]) => {
    const title = group !== section ? `<div class="nav-title">${group}</div>` : '';
    section = group;
    return `${title}<a href="#/${key}" data-page="${key}" data-tip="${text}">${fa(icon)}<span class="nav-text">${text}</span></a>`;
  }).join('');
  if (can('dashboard.view')) api('/dashboard', { params: { days: 30 } }).then(navBadges).catch(() => {});
  // An address left behind by whoever used this browser before may be a section this user cannot see
  const first = NAV.find(n => can(n[2]));
  if (first && !can(currentRoute().entry[2])) location.hash = `#/${first[0]}`;
  route();
}

function signOut() {
  token = null;
  me = null;
  chatLog.length = 0;
  sessionStorage.removeItem('token');
  $('#app').hidden = true;
  $('#pay').hidden = true;
  $('#auth').hidden = false;
  showSwipe(true);
}

async function signIn(email, password) {
  const result = await api('/auth/login', { method: 'POST', body: { email, password } });
  token = result.access_token;
  me = result.user;
  sessionStorage.setItem('token', token);
  showApp();
}

document.querySelectorAll('[data-auth-tab]').forEach(tab => {
  tab.onclick = () => {
    document.querySelectorAll('[data-auth-tab]').forEach(t => t.classList.toggle('active', t === tab));
    $('#login-form').hidden = tab.dataset.authTab !== 'login';
    $('#register-form').hidden = tab.dataset.authTab !== 'register';
    $('#auth-error').textContent = '';
    // The two forms differ in height: start the new one from the top of the card
    $('#auth').scrollTop = 0;
  };
});

function authForm(selector, handler) {
  $(selector).onsubmit = async event => {
    event.preventDefault();
    const button = $('button[type=submit]', event.target);
    button.disabled = true;
    $('#auth-error').textContent = '';
    try {
      await handler(Object.fromEntries(new FormData(event.target)));
      event.target.reset();
    } catch (error) {
      $('#auth-error').textContent = error.message;
    }
    button.disabled = false;
  };
}
authForm('#login-form', values => signIn(values.email, values.password));
authForm('#register-form', async values => {
  const { logo, ...account } = values;
  const picture = logo && logo.size ? logo : null;
  if (picture && picture.size > 512 * 1024) throw new Error('The logo is larger than 512 KB. Choose a smaller picture.');
  await api('/auth/register', { method: 'POST', body: account });
  const result = await api('/auth/login', { method: 'POST', body: { email: account.email, password: account.password } });
  token = result.access_token;
  sessionStorage.setItem('token', token);
  if (picture) {
    // The company exists already: a logo the server refuses is only reported, and can be added later under Users
    const form = new FormData();
    form.append('file', picture);
    await attempt(() => api('/organization/logo', { method: 'PUT', form }));
  }
  me = await api('/auth/me');
  showApp();
});

// Registration form: preview of the chosen logo, and the fee that follows
$('#register-logo').onchange = event => {
  const file = event.target.files[0];
  const preview = $('#register-logo-preview');
  if (preview.src) URL.revokeObjectURL(preview.src);
  setImage(preview, file ? URL.createObjectURL(file) : null);
};
$('#register-form').addEventListener('reset', () => setImage($('#register-logo-preview'), null));
api('/billing/fee').then(({ fee, configured }) => {
  if (fee > 0) $('#register-fee').textContent = configured
    ? `A one-time registration fee of ${rupees(fee)} is paid through Razorpay (UPI, card or net banking) in the next step.`
    : 'New companies cannot register yet: payments are not set up on this server.';
}).catch(() => {});

$('#sign-out').onclick = async () => {
  await api('/auth/logout', { method: 'POST' }).catch(() => {});
  signOut();
};

(async () => {
  if (!token) return signOut();
  try {
    me = await api('/auth/me');
    showApp();
  } catch {
    signOut();
  }
})();

// ---------- shell: layout behaviour only, no data ----------

const appRoot = $('#app');
const isDrawer = () => matchMedia('(max-width: 980px)').matches;

// Chart text in the interface font
if (window.Chart) {
  Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
  Chart.defaults.color = '#5b6472';
}

// Sidebar: icon rail on desktop (remembered), drawer on small screens
function setRail(on) {
  appRoot.classList.toggle('rail', on);
  hideTip();
  try { localStorage.setItem('sidebar-rail', on ? '1' : '0'); } catch { /* storage unavailable: not remembered */ }
}
try { appRoot.classList.toggle('rail', localStorage.getItem('sidebar-rail') === '1'); } catch { /* same */ }
const setDrawer = open => appRoot.classList.toggle('drawer-open', open);
$('#rail-toggle').onclick = () => (isDrawer() ? setDrawer(false) : setRail(!appRoot.classList.contains('rail')));
$('#menu-open').onclick = () => setDrawer(true);
$('#drawer-backdrop').onclick = () => setDrawer(false);
$('#nav').addEventListener('click', () => setDrawer(false));

// Rail tooltips. The tip sits outside the zoomed app, so viewport coordinates apply directly.
function showTip(link) {
  if (!link || !appRoot.classList.contains('rail') || isDrawer()) return hideTip();
  const tip = $('#rail-tip');
  const box = link.getBoundingClientRect();
  tip.textContent = link.dataset.tip;
  tip.style.left = `${box.right + 10}px`;
  tip.style.top = `${box.top + box.height / 2}px`;
  tip.hidden = false;
}
function hideTip() { $('#rail-tip').hidden = true; }
$('#nav').addEventListener('mouseover', event => showTip(event.target.closest('a[data-tip]')));
$('#nav').addEventListener('focusin', event => showTip(event.target.closest('a[data-tip]')));
$('#nav').addEventListener('mouseleave', hideTip);
$('#nav').addEventListener('focusout', hideTip);

// Header search goes to the asset register's own search
$('#hdr-search').onsubmit = event => {
  event.preventDefault();
  const q = $('#hdr-search-input').value.trim();
  location.hash = '#/assets' + (q ? '?' + new URLSearchParams({ q }) : '');
  $('#hdr-search-input').blur();
};

// Spotlight follows the pointer. The header is inside the zoomed app: divide by its zoom.
const hdr = $('#hdr');
hdr.addEventListener('pointermove', event => {
  const zoom = hdr.currentCSSZoom || 1;
  const box = hdr.getBoundingClientRect();
  $('#spotlight').style.transform = `translate(${(event.clientX - box.left) / zoom}px, ${(event.clientY - box.top) / zoom}px)`;
});

// Header photo banner. The gold bar of the current slide is a CSS animation; when it ends the next slide shows,
// so pausing the animation (pointer over the banner, keyboard in it) also pauses the slideshow.
const banner = { index: 0, slides: [...document.querySelectorAll('#banner-track .banner-slide')], bars: [...document.querySelectorAll('#banner-bars button')] };

function showSlide(i) {
  const n = banner.slides.length;
  banner.index = (i + n) % n;
  banner.slides.forEach((slide, k) => {
    slide.classList.toggle('on', k === banner.index);
    slide.setAttribute('aria-hidden', String(k !== banner.index));
  });
  banner.bars.forEach((bar, k) => { bar.classList.remove('on'); bar.classList.toggle('done', k < banner.index); });
  void banner.bars[banner.index].offsetWidth; // restart the fill animation
  banner.bars[banner.index].classList.add('on');
  $('#banner-count').textContent = `${String(banner.index + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`;
}

{
  const box = $('#hdr-banner');
  $('#banner-bars').addEventListener('animationend', event => { if (event.animationName === 'bar-fill') showSlide(banner.index + 1); });
  banner.bars.forEach((bar, k) => { bar.onclick = () => showSlide(k); });
  $('#banner-prev').onclick = () => showSlide(banner.index - 1);
  $('#banner-next').onclick = () => showSlide(banner.index + 1);
  // A clicked button keeps focus: only keyboard focus (focus-visible) holds the slideshow
  const pause = () => box.classList.toggle('paused', box.matches(':hover') || Boolean(box.querySelector(':focus-visible')));
  for (const type of ['mouseenter', 'mouseleave', 'focusin', 'focusout']) box.addEventListener(type, () => setTimeout(pause));
  box.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight') showSlide(banner.index + 1);
    if (event.key === 'ArrowLeft') showSlide(banner.index - 1);
  });
  showSlide(0);
}

// Shift clock: three 8-hour shifts, A 06:00, B 14:00, C 22:00
const SHIFTS = [['A', 'Morning', 6], ['B', 'Evening', 14], ['C', 'Night', 22]];
function currentShift(now = new Date()) {
  const minutes = now.getHours() * 60 + now.getMinutes();
  const [letter, name, startHour] = SHIFTS[minutes >= 22 * 60 || minutes < 6 * 60 ? 2 : minutes >= 14 * 60 ? 1 : 0];
  const elapsed = (minutes - startHour * 60 + 1440) % 1440;
  const left = 480 - elapsed;
  return { letter, name, share: elapsed / 480, left: `${Math.floor(left / 60)}h ${left % 60}m` };
}
function tickShift() {
  const now = new Date();
  const shift = currentShift(now);
  $('#shift-name').textContent = `Shift ${shift.letter} · ${shift.name}`;
  $('#shift-time').textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
  $('#shift-fill').style.width = `${shift.share * 100}%`;
  $('#shift-left').textContent = `${shift.left} left in shift`;
}
tickShift();
setInterval(tickShift, 15000);

document.addEventListener('keydown', event => {
  if (!(event.ctrlKey || event.metaKey)) {
    if (event.key === 'Escape') setDrawer(false);
    return;
  }
  const key = event.key.toLowerCase();
  if (['+', '-', '=', '_'].includes(key)) { event.preventDefault(); return; } // fixed scale; Ctrl+0 still resets
  if (appRoot.hidden) return;
  if (key === 'k') { event.preventDefault(); $('#hdr-search-input').focus(); }
  if (key === 'b' && !isDrawer()) { event.preventDefault(); setRail(!appRoot.classList.contains('rail')); }
});
window.addEventListener('wheel', event => { if (event.ctrlKey) event.preventDefault(); }, { passive: false });

// Sign-in: swipe (or press the thumb) to reveal the form
function showSwipe(on) {
  $('#swipe').hidden = !on;
  $('#auth-forms').hidden = on;
  $('#swipe-thumb').style.transform = '';
  $('#auth-error').textContent = '';
  $('#auth').scrollTop = 0;
  if (!on) $('#auth-forms form:not([hidden]) input').focus({ preventScroll: true });
}
{
  const swipe = $('#swipe');
  const thumb = $('#swipe-thumb');
  let dragFrom = null;
  let dragged = 0;
  const room = () => swipe.clientWidth - thumb.offsetWidth - 8;
  thumb.addEventListener('pointerdown', event => {
    dragFrom = event.clientX;
    dragged = 0;
    swipe.classList.add('dragging');
    thumb.setPointerCapture(event.pointerId);
  });
  thumb.addEventListener('pointermove', event => {
    if (dragFrom === null) return;
    dragged = Math.max(0, Math.min(event.clientX - dragFrom, room()));
    thumb.style.transform = `translateX(${dragged}px)`;
  });
  const endDrag = () => {
    if (dragFrom === null) return;
    dragFrom = null;
    swipe.classList.remove('dragging');
    if (dragged > room() * 0.85) showSwipe(false);
    else thumb.style.transform = '';
  };
  thumb.addEventListener('pointerup', endDrag);
  thumb.addEventListener('pointercancel', endDrag);
  // A plain click or Enter/Space works too, so the form never depends on dragging
  thumb.addEventListener('click', () => { if (dragged < 4) showSwipe(false); });
  document.querySelectorAll('[data-swipe-back]').forEach(button => { button.onclick = () => showSwipe(true); });
}
