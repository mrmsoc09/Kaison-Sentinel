async function loadPlaybooks() {
  const el = document.getElementById('playbookList');
  if (!el) return;
  try {
    const res = await fetch('/api/assets/playbooks');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'Failed to load playbooks.';
  }
}

async function addPlaybook() {
  const id = document.getElementById('playbookId').value.trim();
  const name = document.getElementById('playbookName').value.trim();
  const modules = document.getElementById('playbookModules').value.split(',').map(s => s.trim()).filter(Boolean);
  const status = document.getElementById('playbookStatus');
  if (!id || !name || modules.length === 0) {
    status.textContent = 'id, name, and modules required.';
    return;
  }
  try {
    const res = await fetch('/api/playbooks/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, name, modules })
    });
    const data = await res.json();
    status.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    status.textContent = 'Playbook add error.';
  }
}

async function exportPlaybooks() {
  const out = document.getElementById('playbookExport');
  try {
    const res = await fetch('/api/playbooks/export');
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Export error.';
  }
}

async function importPlaybooks() {
  const fmt = document.getElementById('playbookImportFormat').value;
  const data = document.getElementById('playbookImportData').value;
  const out = document.getElementById('playbookImportStatus');
  try {
    const res = await fetch('/api/playbooks/import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ format: fmt, data })
    });
    const json = await res.json();
    out.textContent = JSON.stringify(json, null, 2);
  } catch (e) {
    out.textContent = 'Import error.';
  }
}

window.addEventListener('load', () => {
  loadPlaybooks();
  const btn = document.getElementById('playbookAdd');
  if (btn) btn.addEventListener('click', addPlaybook);
  const exp = document.getElementById('playbookExportBtn');
  if (exp) exp.addEventListener('click', exportPlaybooks);
  const imp = document.getElementById('playbookImportBtn');
  if (imp) imp.addEventListener('click', importPlaybooks);
});
