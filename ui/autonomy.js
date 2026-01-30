async function loadAutonomyStatus() {
  const el = document.getElementById('autonomyStatus');
  if (!el) return;
  try {
    const [hwRes, progRes] = await Promise.all([
      fetch('/api/hardware'),
      fetch('/api/programs/sync/status')
    ]);
    const hw = await hwRes.json();
    const prog = await progRes.json();
    el.textContent = JSON.stringify({ hardware: hw, program_sync: prog }, null, 2);
  } catch (e) {
    el.textContent = 'Autonomy status unavailable.';
  }
}

async function runAutoRepair() {
  const el = document.getElementById('autonomyStatus');
  try {
    const res = await fetch('/api/autonomy/repair');
    const data = await res.json();
    if (el) el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    if (el) el.textContent = 'Auto-repair failed.';
  }
}

window.addEventListener('load', () => {
  loadAutonomyStatus();
  setInterval(loadAutonomyStatus, 60000);
  const btn = document.getElementById('autoRepairBtn');
  if (btn) btn.addEventListener('click', runAutoRepair);
});
