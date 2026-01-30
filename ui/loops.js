function _badge(status) {
  if (status === 'ok') return '✅';
  if (status === 'warn') return '⚠️';
  if (status === 'blocked') return '⛔';
  return '•';
}

window.loadLoopState = async function () {
  const out = document.getElementById('loopState');
  if (!out) return;
  const runId = document.getElementById('runIdLookup')?.value.trim();
  try {
    const url = runId ? `/api/loops/state?run_id=${encodeURIComponent(runId)}` : '/api/loops/state';
    const res = await fetch(url);
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Loop state fetch error.';
  }
};

window.loadLoopAudit = async function () {
  const out = document.getElementById('loopAudit');
  if (!out) return;
  const runId = document.getElementById('runIdLookup')?.value.trim();
  try {
    const url = runId ? `/api/loops/state?run_id=${encodeURIComponent(runId)}` : '/api/loops/state';
    const res = await fetch(url);
    const data = await res.json();
    if (!data || !data.loops) {
      out.textContent = 'No loop state available.';
      return;
    }
    const lines = [];
    for (const [name, info] of Object.entries(data.loops)) {
      const status = info.status || 'unknown';
      const action = info.action || '';
      lines.push(`${_badge(status)} ${name} → ${status}${action ? ` · next: ${action}` : ''}`);
    }
    out.textContent = lines.join('\n');
  } catch (e) {
    out.textContent = 'Loop audit fetch error.';
  }
};

window.addEventListener('load', () => {
  if (window.loadLoopState) window.loadLoopState();
  if (window.loadLoopAudit) window.loadLoopAudit();
});
