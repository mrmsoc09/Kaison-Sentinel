const btn = document.getElementById('searchBtn');
const results = document.getElementById('results');
const planBtn = document.getElementById('planBtn');
const planOut = document.getElementById('planOut');

const vaultRefresh = document.getElementById('vaultRefresh');
const vaultProviders = document.getElementById('vaultProviders');
const vaultAdd = document.getElementById('vaultAdd');
const vaultStatus = document.getElementById('vaultStatus');
const outputsRefresh = document.getElementById('outputsRefresh');
const traceList = document.getElementById('traceList');
const evalList = document.getElementById('evalList');
const bqList = document.getElementById('bqList');

async function refreshOutputs() {
  const runId = document.getElementById('runIdLookup')?.value.trim();
  try {
    const t = await fetch('/api/outputs/traces');
    const tdata = await t.json();
    if (traceList) traceList.textContent = JSON.stringify(tdata, null, 2);
  } catch (e) {
    if (traceList) traceList.textContent = 'Trace fetch error.';
  }

  try {
    const e = await fetch('/api/outputs/evals');
    const edata = await e.json();
    if (evalList) evalList.textContent = JSON.stringify(edata, null, 2);
  } catch (e) {
    if (evalList) evalList.textContent = 'Eval fetch error.';
  }

  try {
    const url = runId ? `/api/outputs/bigquery?run_id=${encodeURIComponent(runId)}` : '/api/outputs/bigquery';
    const b = await fetch(url);
    const bdata = await b.json();
    if (bqList) bqList.textContent = JSON.stringify(bdata, null, 2);
  } catch (e) {
    if (bqList) bqList.textContent = 'BigQuery export fetch error.';
  }
  if (window.loadLoopState) window.loadLoopState();
  if (window.loadLoopAudit) window.loadLoopAudit();
}

async function doSearch() {
  const q = document.getElementById('query').value.trim();
  if (!q) {
    results.textContent = 'Enter a query.';
    return;
  }
  results.textContent = 'Searching...';
  try {
    const res = await fetch(`/search?q=${encodeURIComponent(q)}&k=5`);
    const data = await res.json();
    results.innerHTML = '';
    (data.results || []).forEach((r) => {
      const div = document.createElement('div');
      div.className = 'card';
      div.textContent = `${r.score.toFixed(3)} · ${r.text.slice(0, 160)}`;
      results.appendChild(div);
    });
    if (!data.results || data.results.length === 0) {
      results.textContent = 'No matches.';
    }
  } catch (e) {
    results.textContent = 'Search error.';
  }
}

async function doPlan() {
  if (!planOut) return;
  planOut.textContent = 'Planning...';
  const goal = document.getElementById('planGoal').value.trim();
  const targets = document.getElementById('planTargets').value.split(',').map(s => s.trim()).filter(Boolean);
  const constraints = document.getElementById('planConstraints').value.trim();
  const playbooks = document.getElementById('planPlaybooks')?.value
    .split(',')
    .map(s => s.trim())
    .filter(Boolean);
  const mitreId = document.getElementById('planMitre')?.value.trim();
  const budgetTier = document.getElementById('planBudgetTier')?.value;
  const dailyBudget = parseFloat(document.getElementById('planBudgetDaily')?.value || '');
  const stealth = document.getElementById('planStealth')?.value;
  const durationDays = parseInt(document.getElementById('planDuration')?.value || '', 10);
  const poolSize = parseInt(document.getElementById('planPoolSize')?.value || '', 10);
  const activeLimit = parseInt(document.getElementById('planActiveLimit')?.value || '', 10);
  const autoInstall = document.getElementById('planAutoInstall')?.checked;
  const kind = document.getElementById('planKind').value;
  const role = document.getElementById('planRole').value;
  const reportFormat = document.getElementById('reportFormat')?.value;

  try {
    const res = await fetch('/api/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scope: {
          allowlist: targets,
          goal: goal,
          constraints: constraints,
          playbook_ids: playbooks || [],
          mitre_technique_id: mitreId || undefined,
          budget_tier: budgetTier || undefined,
          daily_budget_usd: Number.isFinite(dailyBudget) ? dailyBudget : undefined,
          stealth: stealth || undefined,
          scan_duration_days: Number.isFinite(durationDays) ? durationDays : undefined,
          scan_pool_size: Number.isFinite(poolSize) ? poolSize : undefined,
          max_active_scans: Number.isFinite(activeLimit) ? activeLimit : undefined,
          auto_install_tools: !!autoInstall,
          allow_install: !!autoInstall,
          module_kind: kind,
          role: role,
          report_format_id: reportFormat || undefined
        }
      })
    });
    const data = await res.json();
    planOut.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    planOut.textContent = 'Plan error.';
  }
}

async function refreshVault() {
  if (!vaultProviders) return;
  try {
    const res = await fetch('/api/vault/providers');
    const data = await res.json();
    vaultProviders.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    vaultProviders.textContent = 'Vault error.';
  }
}

async function addVaultKey() {
  if (!vaultStatus) return;
  const sourceId = document.getElementById('vaultSource').value.trim();
  const key = document.getElementById('vaultKey').value.trim();
  if (!sourceId || !key) {
    vaultStatus.textContent = 'Source id and key required.';
    return;
  }
  try {
    const res = await fetch('/api/vault/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source_id: sourceId, key })
    });
    const data = await res.json();
    vaultStatus.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    vaultStatus.textContent = 'Vault add error.';
  }
}

async function loadReportFormats() {
  const sel = document.getElementById('reportFormat');
  if (!sel) return;
  try {
    const res = await fetch('/api/assets/report_formats');
    const data = await res.json();
    sel.innerHTML = '';
    data.forEach((f) => {
      const opt = document.createElement('option');
      opt.value = f.id;
      opt.textContent = f.id;
      sel.appendChild(opt);
    });
  } catch (e) {
    // ignore
  }
}

if (btn) btn.addEventListener('click', doSearch);
if (planBtn) planBtn.addEventListener('click', doPlan);
if (vaultRefresh) vaultRefresh.addEventListener('click', refreshVault);
if (vaultAdd) vaultAdd.addEventListener('click', addVaultKey);
if (outputsRefresh) outputsRefresh.addEventListener('click', refreshOutputs);

window.addEventListener('load', loadReportFormats);
window.addEventListener('load', refreshOutputs);
