async function loadRunHistory() {
  const el = document.getElementById('runHistory');
  if (!el) return;
  try {
    const res = await fetch('/api/runs/history?limit=25');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'Failed to load run history.';
  }
}

window.addEventListener('load', () => {
  loadRunHistory();
});
