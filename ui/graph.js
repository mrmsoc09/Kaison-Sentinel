async function loadGraph() {
  const el = document.getElementById('graphView');
  if (!el) return;
  try {
    const res = await fetch('/api/graph/latest');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'Graph load error.';
  }
}

window.addEventListener('load', () => {
  loadGraph();
});
