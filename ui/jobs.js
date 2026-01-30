async function loadJobQueue() {
  const el = document.getElementById('jobQueue');
  if (!el) return;
  try {
    const res = await fetch('/api/jobs');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'Failed to load job queue.';
  }
}

window.addEventListener('load', () => {
  loadJobQueue();
  setInterval(loadJobQueue, 5000);
});
