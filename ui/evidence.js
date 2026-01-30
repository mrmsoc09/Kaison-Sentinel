async function attachEvidence() {
  const out = document.getElementById('evidenceStatus');
  const runId = document.getElementById('evidenceRunId').value.trim();
  const findingId = document.getElementById('evidenceFindingId').value.trim();
  const kind = document.getElementById('evidenceKind').value.trim();
  const path = document.getElementById('evidencePath').value.trim();
  if (!runId || !findingId || !path) {
    out.textContent = 'run_id, finding_id, and path required.';
    return;
  }
  try {
    const res = await fetch('/api/evidence/attach', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ run_id: runId, finding_id: findingId, kind, path })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Evidence attach error.';
  }
}

window.addEventListener('load', () => {
  const btn = document.getElementById('evidenceAttachBtn');
  if (btn) btn.addEventListener('click', attachEvidence);
});
