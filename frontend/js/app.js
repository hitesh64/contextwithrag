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
};
const MOVE_LABEL = {
  pending_approval: 'Submit for approval', approved: 'Approve', rejected: 'Reject', draft: 'Back to draft',
  in_progress: 'Start work', completed: 'Mark completed', cancelled: 'Cancel work order',
};

let token = sessionStorage.getItem('token');
let me = null;
let chart = null;
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
const can = role => me && ROLES.indexOf(me.role) >= ROLES.indexOf(role);

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
        if (f.type === 'file') values[f.name] = el.files[0];
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
  const data = await api('/assets', { params: { page_size: 200 } });
  return data.items.map(a => [a.id, `${a.asset_code} — ${a.name}`]);
}

/** Open an original document through the authenticated API (there is no public file URL). */
async function openDocument(id, pageNumber) {
  await attempt(async () => {
    const response = await api(`/documents/${id}/file`, { raw: true });
    const url = URL.createObjectURL(await response.blob());
    window.open(url + (pageNumber ? `#page=${pageNumber}` : ''), '_blank', 'noopener');
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  });
}

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

// [page, label, minimum role, icon, sidebar section]
const NAV = [
  ['dashboard', 'Dashboard', 'viewer', 'gauge-high', 'Main'], ['chat', 'Ask', 'viewer', 'comments', 'Main'],
  ['assets', 'Assets', 'viewer', 'industry', 'Maintenance'], ['documents', 'Documents', 'viewer', 'book-open', 'Maintenance'],
  ['breakdowns', 'Breakdowns', 'viewer', 'triangle-exclamation', 'Maintenance'], ['work-orders', 'Work orders', 'viewer', 'clipboard-list', 'Maintenance'],
  ['conflicts', 'Conflicts', 'viewer', 'code-compare', 'Maintenance'],
  ['audit', 'Audit history', 'maintenance_manager', 'clock-rotate-left', 'Administration'], ['users', 'Users', 'admin', 'users', 'Administration'],
];
const fa = name => `<i class="fa-solid fa-${name}"></i>`;

/** Count pills in the sidebar, from the same figures the dashboard shows. */
function navBadges(d) {
  const counts = { 'work-orders': d.work_orders.pending_approval || 0, breakdowns: (d.breakdowns.open || 0) + (d.breakdowns.in_progress || 0) };
  for (const [key, count] of Object.entries(counts)) {
    const link = $(`#nav a[data-page="${key}"]`);
    if (!link) continue;
    $('.nav-badge', link)?.remove();
    if (count) link.insertAdjacentHTML('beforeend', `<span class="nav-badge">${count}</span>`);
  }
}
const pages = {};
let actions = {};

pages.dashboard = async (_, query) => {
  const days = query.get('days') || '90';
  const d = await api('/dashboard', { params: { days } });
  const sum = counts => Object.values(counts).reduce((a, b) => a + b, 0);
  const stat = (value, text, href, tone, icon) => `<a class="stat tone-${tone}" href="${href}"><div class="stat-icon">${fa(icon)}</div>
    <div class="label">${esc(text)}</div><div class="value">${value}</div><div class="stat-art" aria-hidden="true">${fa(icon)}</div></a>`;
  navBadges(d);
  const period = `${day(d.period_start)} – ${day(new Date())}`;
  page().innerHTML = `
    <div class="page-head"><h1>Dashboard</h1>
      <label>Period <select id="days">${[['30', 'Last 30 days'], ['90', 'Last 90 days'], ['365', 'Last 12 months']].map(([v, t]) => `<option value="${v}" ${v === days ? 'selected' : ''}>${t}</option>`).join('')}</select></label></div>
    <div class="grid">
      ${stat(sum(d.assets) - (d.assets.archived || 0), 'Assets in the register', '#/assets', 'blue', 'industry')}
      ${stat(d.documents.ready || 0, 'Documents ready to search', '#/documents', 'green', 'book-open')}
      ${stat(d.documents.failed || 0, 'Documents that failed processing', '#/documents?status=failed', 'red', 'file-circle-xmark')}
      ${stat((d.breakdowns.open || 0) + (d.breakdowns.in_progress || 0), 'Unresolved breakdowns', '#/breakdowns?status=open', 'amber', 'triangle-exclamation')}
      ${stat(d.work_orders.pending_approval || 0, 'Work orders awaiting approval', '#/work-orders?status=pending_approval', 'purple', 'clipboard-check')}
      ${stat(`${d.questions_unanswered} / ${d.questions_asked}`, `Questions without evidence (${period})`, '#/dashboard', 'teal', 'circle-question')}
    </div>
    <div class="chart-grid"><div class="card"><h2>${fa('chart-bar')}Downtime by asset</h2>
      <p class="hint">Recorded downtime in minutes, breakdowns reported ${esc(period)}. Records without a downtime value count as 0.</p>
      ${d.downtime_by_asset.length ? '<div class="chart-box"><canvas id="downtime" aria-label="Downtime by asset" role="img"></canvas></div>' : '<div class="empty">No breakdowns recorded in this period.</div>'}
    </div>
    ${can('maintenance_manager') ? `<div class="card" id="unanswered"><h2>${fa('circle-question')}Questions the records could not answer</h2>
      <p class="hint">Each one points at a manual, SOP or record that is missing from the library.</p><div id="unanswered-list"></div></div>` : ''}</div>`;
  $('#days').onchange = event => { location.hash = `#/dashboard?days=${event.target.value}`; };

  if (d.downtime_by_asset.length) {
    if (window.Chart) {
      chart = new Chart($('#downtime'), {
        type: 'bar',
        data: { labels: d.downtime_by_asset.map(a => a.asset_code), datasets: [{ label: 'Downtime (minutes)', data: d.downtime_by_asset.map(a => a.downtime_minutes), backgroundColor: '#2563eb', borderRadius: 6, maxBarThickness: 22 }] },
        options: {
          indexAxis: 'y',
          maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { callbacks: { afterLabel: ctx => `${d.downtime_by_asset[ctx.dataIndex].breakdowns} breakdown(s)` } } },
          scales: { x: { beginAtZero: true, title: { display: true, text: 'Downtime (minutes)' }, grid: { color: 'rgba(15,23,42,0.05)' } }, y: { title: { display: true, text: 'Asset' }, grid: { display: false } } },
        },
      });
    } else {
      // The chart library could not be loaded: the same figures as a table
      $('.chart-box').outerHTML = table([
        { title: 'Asset', cell: a => esc(a.asset_code) }, { title: 'Downtime (min)', num: true, cell: a => a.downtime_minutes },
        { title: 'Breakdowns', num: true, cell: a => a.breakdowns },
      ], d.downtime_by_asset);
    }
  }
  if (can('maintenance_manager')) {
    const missing = await api('/chat/unanswered', { params: { page_size: 10 } });
    $('#unanswered-list').innerHTML = table([
      { title: 'Asked', cell: q => when(q.created_at) }, { title: 'By', cell: q => esc(q.user_name) }, { title: 'Question', cell: q => esc(q.question) },
    ], missing.items, { empty: 'No unanswered questions so far.' });
  }
};

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
    <div class="page-head"><h1>Asset register</h1>
      ${can('maintenance_manager') ? '<button class="btn primary" data-action="add-asset">Add asset</button>' : ''}</div>
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
  const gaps = s.data_gaps;
  page().innerHTML = `
    <div class="page-head"><div><a href="#/assets">← Assets</a><h1>${esc(a.asset_code)} — ${esc(a.name)}</h1></div>
      <div class="actions">
        <a class="btn" href="#/chat?asset=${esc(a.id)}">Ask about this asset</a>
        ${can('technician') ? '<button class="btn primary" data-action="draft-wo">Draft work order</button>' : ''}
        ${can('maintenance_manager') ? '<button class="btn" data-action="edit-asset">Edit</button>' : ''}
        ${can('maintenance_manager') && a.status !== 'archived' ? '<button class="btn danger" data-action="archive-asset">Archive</button>' : ''}
      </div></div>
    <div class="two-col">
      <div class="card"><h2>${fa('circle-info')}Details</h2><dl class="kv">
        <dt>Status</dt><dd>${badge(a.status)}</dd><dt>Criticality</dt><dd>${badge(a.criticality)}</dd>
        <dt>Type</dt><dd>${shown(a.asset_type)}</dd><dt>Manufacturer</dt><dd>${shown(a.manufacturer)}</dd>
        <dt>Model</dt><dd>${shown(a.model)}</dd><dt>Serial number</dt><dd>${shown(a.serial_number)}</dd>
        <dt>Location</dt><dd>${shown(a.location)}</dd></dl></div>
      <div class="card"><h2>${fa('chart-simple')}Breakdown history: recorded facts</h2>
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
      </div>
    </div>
    <div class="card"><h2>${fa('book-open')}Linked documents</h2>${table([
      { title: 'File', cell: d => `<a href="#" data-action="open-doc" data-id="${esc(d.id)}">${esc(d.filename)}</a>` },
      { title: 'Type', cell: d => label(d.doc_type) }, { title: 'Status', cell: d => badge(d.status) },
    ], a.documents, { empty: 'No document is linked to this asset. Upload its manual or SOP under Documents.' })}</div>
    <div class="card"><h2>${fa('triangle-exclamation')}Recent breakdowns</h2>${breakdownTable(a.recent_breakdowns, false)}</div>
    <div class="card"><h2>${fa('clipboard-list')}Work orders</h2>${workOrderTable(a.work_orders)}</div>`;
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
      ${can('maintenance_manager') ? '<button class="btn primary" data-action="upload">Upload document</button>' : ''}</div>
    <form class="filters" id="filters"><label>Status<select name="status">${['', 'ready', 'queued', 'processing', 'failed'].map(v => `<option value="${v}" ${v === params.status ? 'selected' : ''}>${v ? label(v) : 'All'}</option>`).join('')}</select></label>
      <button class="btn" type="submit">Apply</button></form>
    ${table([
      { title: 'File', cell: d => `<a href="#" data-action="open-doc" data-id="${esc(d.id)}">${esc(d.filename)}</a><div class="hint">${(d.size_bytes / 1024).toFixed(0)} KB · uploaded ${when(d.created_at)} by ${esc(d.uploaded_by_name)}</div>` },
      { title: 'Type', cell: d => label(d.doc_type) },
      { title: 'Assets', cell: d => d.asset_ids.length ? d.asset_ids.map(i => esc(names[i] || 'archived asset')).join(', ') : '<span class="muted">General</span>' },
      { title: 'Status', cell: d => `${badge(d.status)}${d.error ? `<div class="hint" style="color:var(--bad)">${esc(d.error)}</div>` : ''}` },
      { title: 'Indexed', num: true, cell: d => d.status === 'ready' ? `${d.chunk_count} sections${d.page_count ? ` · ${d.page_count} pages` : ''}` : '—' },
      { title: '', cell: d => can('maintenance_manager') ? `<div class="actions">
          ${['failed', 'ready'].includes(d.status) ? `<button class="btn small" data-action="reprocess" data-id="${esc(d.id)}">Reprocess</button>` : ''}
          <button class="btn small danger" data-action="delete-doc" data-id="${esc(d.id)}" data-name="${esc(d.filename)}">Delete</button></div>` : '' },
    ], data.items, { empty: 'No documents yet. Upload a machine manual or SOP (PDF, DOCX, PPTX, TXT).' })}
    ${pager(data, 'docs-page')}`;
  $('#filters').onsubmit = event => { event.preventDefault(); location.hash = '#/documents?' + new URLSearchParams(new FormData(event.target)); };
  actions['docs-page'] = el => { query.set('page', el.dataset.page); location.hash = '#/documents?' + query; };
  actions.upload = async () => {
    const done = await formDialog({
      title: 'Upload document', submitLabel: 'Upload',
      note: 'Processing runs in the background; the status column shows when the document is ready to search.',
      fields: [
        { name: 'file', label: 'File', type: 'file', required: true, accept: '.pdf,.docx,.pptx,.txt,.md', hint: 'PDF, DOCX, PPTX, TXT or MD with selectable text. Scanned pages are not supported yet.' },
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
    ...(can('technician') ? [{ title: '', cell: b => `<button class="btn small" data-action="edit-breakdown" data-id="${esc(b.id)}">Update</button>` }] : []),
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
      ${can('maintenance_manager') ? '<button class="btn" data-action="import">Import CSV / XLSX</button>' : ''}
      ${can('technician') ? '<button class="btn primary" data-action="add-breakdown">Report breakdown</button>' : ''}</div></div>
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
    note: 'With “Generate from records”, the draft is built from this asset’s SOPs and breakdown history and shows its sources. It is only a draft: nothing happens until a manager approves it.',
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
    <div class="page-head"><h1>Work orders</h1>
      ${can('technician') ? '<button class="btn primary" data-action="new-wo">Draft work order</button>' : ''}</div>
    <div class="tabs">${tabs.map(([v, t]) => `<a class="tab ${v === status ? 'active' : ''}" href="#/work-orders${v ? '?status=' + v : ''}">${t}</a>`).join('')}</div>
    ${workOrderTable(data.items)}${pager(data, 'wo-page')}`;
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
    ${w.status === 'draft' ? `<div class="notice">This is a draft${w.generated ? ' generated from your records' : ''}. Nothing is carried out until it is submitted and approved by a manager${w.generated ? '; check every step against its source first' : ''}.</div>` : ''}
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
      The assistant never picks one. A maintenance manager or administrator records which applies; everyone can see the decision.
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
          ${c.status === 'open' && can('maintenance_manager') ? `<button class="btn primary small" data-action="resolve-conflict" data-id="${esc(c.id)}">Record a decision</button>` : ''}</div>
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
      <label>Record type<select name="resource_type">${['', 'work_order', 'document', 'conflict', 'asset', 'breakdown', 'user', 'organization'].map(v => `<option value="${v}" ${v === params.resource_type ? 'selected' : ''}>${v ? label(v) : 'All'}</option>`).join('')}</select></label>
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
  const data = await api('/users');
  const roleOptions = ROLES.map(r => [r, ROLE_NAMES[r]]);
  page().innerHTML = `
    <div class="page-head"><h1>Users</h1><button class="btn primary" data-action="add-user">Add user</button></div>
    <div class="notice">Viewer: read and ask. Technician: also report breakdowns, draft work orders and carry out approved ones.
      Maintenance manager: also manage assets and documents, import records and approve work orders. Administrator: also manage users.</div>
    ${table([
      { title: 'Name', cell: u => esc(u.name) }, { title: 'Email', cell: u => esc(u.email) },
      { title: 'Role', cell: u => esc(ROLE_NAMES[u.role]) }, { title: 'Status', cell: u => badge(u.is_active ? 'active' : 'inactive') },
      { title: '', cell: u => u.id === me.id ? '<span class="muted">you</span>' : `<div class="actions">
          <button class="btn small" data-action="role" data-id="${esc(u.id)}" data-role="${u.role}" data-name="${esc(u.name)}">Change role</button>
          <button class="btn small ${u.is_active ? 'danger' : ''}" data-action="toggle-user" data-id="${esc(u.id)}" data-active="${u.is_active}">${u.is_active ? 'Deactivate' : 'Activate'}</button></div>` },
    ], data.items)}`;
  actions['add-user'] = async () => {
    if (await formDialog({
      title: 'Add user', submitLabel: 'Add user',
      fields: [
        { name: 'name', label: 'Name', required: true, minlength: 2 }, { name: 'email', label: 'Email', type: 'email', required: true },
        { name: 'password', label: 'Initial password', type: 'password', required: true, minlength: 8, hint: 'At least 8 characters. Give it to the user personally.' },
        { name: 'role', label: 'Role', type: 'select', options: roleOptions, value: 'technician' },
      ],
      submit: values => api('/users', { method: 'POST', body: values }),
    })) route();
  };
  actions.role = async el => {
    if (await formDialog({
      title: `Role of ${el.dataset.name}`, fields: [{ name: 'role', label: 'Role', type: 'select', options: roleOptions, value: el.dataset.role }],
      submit: values => api(`/users/${el.dataset.id}`, { method: 'PATCH', body: values }),
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

async function route() {
  clearTimeout(pollTimer);
  if (chart) { chart.destroy(); chart = null; }
  const [path, search = ''] = location.hash.replace(/^#\/?/, '').split('?');
  const [name = 'dashboard', id] = path.split('/');
  const entry = NAV.find(n => n[0] === (name || 'dashboard')) || NAV[0];
  actions = { ...sharedActions };
  document.querySelectorAll('#nav a').forEach(a => a.classList.toggle('active', a.dataset.page === entry[0]));
  if (!can(entry[2])) {
    page().innerHTML = '<div class="empty">Your role does not have access to this page.</div>';
    return;
  }
  try {
    await pages[entry[0]](id, new URLSearchParams(search));
    const heading = $('.page-head h1');
    if (heading && !heading.querySelector('i')) heading.insertAdjacentHTML('afterbegin', fa(entry[3]));
  } catch (error) {
    if (token) page().innerHTML = `<div class="card"><h2>${fa('circle-exclamation')}This page could not be loaded</h2><p class="error">${esc(error.message)}</p><button class="btn" data-action="retry">Try again</button></div>`;
    actions.retry = route;
  }
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

function showApp() {
  $('#auth').hidden = true;
  $('#app').hidden = false;
  $('#org-name').textContent = me.organization_name;
  $('#who-name').textContent = me.name;
  $('#who-role').textContent = ROLE_NAMES[me.role];
  $('#who-avatar').textContent = me.name.trim().charAt(0);
  let section = '';
  $('#nav').innerHTML = NAV.filter(n => can(n[2])).map(([key, text, , icon, group]) => {
    const title = group !== section ? `<div class="nav-title">${group}</div>` : '';
    section = group;
    return `${title}<a href="#/${key}" data-page="${key}" data-tip="${text}">${fa(icon)}<span class="nav-text">${text}</span></a>`;
  }).join('');
  api('/dashboard', { params: { days: 30 } }).then(navBadges).catch(() => {});
  route();
}

function signOut() {
  token = null;
  me = null;
  chatLog.length = 0;
  sessionStorage.removeItem('token');
  $('#app').hidden = true;
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
  await api('/auth/register', { method: 'POST', body: values });
  await signIn(values.email, values.password);
});

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
  if (!on) $('#auth-forms form:not([hidden]) input').focus();
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
