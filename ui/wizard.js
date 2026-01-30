async function loadWizard() {
  const el = document.getElementById('wizardSteps');
  if (!el) return;
  try {
    const res = await fetch('/wizard.json');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'Wizard load error.';
  }
}

window.addEventListener('load', () => {
  loadWizard();
});
