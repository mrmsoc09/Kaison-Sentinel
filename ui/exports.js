async function exportBundle() {
  const out = document.getElementById('exportStatus');
  const runId = document.getElementById('exportRunId').value.trim();
  if (!runId) {
    out.textContent = 'run_id required.';
    return;
  }
  try {
    const res = await fetch(`/api/exports/bundle?run_id=${encodeURIComponent(runId)}`);
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Export error.';
  }
}

window.addEventListener('load', () => {
  const btn = document.getElementById('exportBundleBtn');
  if (btn) btn.addEventListener('click', exportBundle);
});
