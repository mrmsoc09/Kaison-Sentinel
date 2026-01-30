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

window.addEventListener('load', () => {
  loadAutonomyStatus();
  setInterval(loadAutonomyStatus, 60000);
});
