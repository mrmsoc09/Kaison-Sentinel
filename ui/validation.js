async function loadValidationChecklist() {
  const el = document.getElementById('validationChecklist');
  if (!el) return;
  try {
    const res = await fetch('/api/validation/checklist');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'Validation checklist load error.';
  }
}

window.addEventListener('load', () => {
  loadValidationChecklist();
});
