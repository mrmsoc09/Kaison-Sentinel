async function loadSchedulerStatus() {
  const el = document.getElementById('schedulerStatus');
  if (!el) return;
  try {
    const res = await fetch('/api/scheduler/status');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'Scheduler status unavailable.';
  }
}

async function parseScopes() {
  try {
    await fetch('/api/programs/parse', { method: 'POST' });
  } catch (e) {
    // ignore
  }
  loadSchedulerStatus();
}

async function previewSchedule() {
  try {
    const res = await fetch('/api/scheduler/preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scope: { module_kind: 'osint' } })
    });
    const data = await res.json();
    const el = document.getElementById('schedulerStatus');
    if (el) el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    // ignore
  }
}

async function runSchedule() {
  try {
    const res = await fetch('/api/scheduler/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scope: { module_kind: 'osint' } })
    });
    const data = await res.json();
    const el = document.getElementById('schedulerStatus');
    if (el) el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    // ignore
  }
}

window.addEventListener('load', () => {
  const parseBtn = document.getElementById('parseScopesBtn');
  const previewBtn = document.getElementById('schedulerPreviewBtn');
  const runBtn = document.getElementById('schedulerRunBtn');
  if (parseBtn) parseBtn.addEventListener('click', parseScopes);
  if (previewBtn) previewBtn.addEventListener('click', previewSchedule);
  if (runBtn) runBtn.addEventListener('click', runSchedule);
  loadSchedulerStatus();
});
