async function loadSetupHub() {
  const el = document.getElementById('setupHub');
  if (!el) return;
  try {
    const res = await fetch('/api/setup/hub');
    const data = await res.json();
    const statusRes = await fetch('/api/programs/sync/status');
    const status = await statusRes.json();
    renderSetupHub(el, data.steps || [], status);
  } catch (e) {
    el.textContent = 'Failed to load setup hub.';
  }
}

async function updateSetupStep(stepId, status) {
  try {
    await fetch('/api/setup/hub', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ step_id: stepId, status })
    });
  } catch (e) {
    // ignore
  }
}

async function triggerProgramSync() {
  try {
    await fetch('/api/programs/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ force: true })
    });
  } catch (e) {
    // ignore
  }
  loadSetupHub();
}

function renderSetupHub(el, steps, programStatus) {
  el.innerHTML = '';
  if (!steps.length) {
    el.textContent = 'No setup steps configured.';
    return;
  }
  steps.forEach((step) => {
    const row = document.createElement('div');
    row.className = 'setup-row';
    const title = document.createElement('div');
    title.className = 'setup-title';
    title.textContent = step.title || step.id;
    const notes = document.createElement('div');
    notes.className = 'setup-notes';
    notes.textContent = step.notes || '';
    const status = document.createElement('select');
    status.className = 'setup-status';
    ['todo', 'in_progress', 'done'].forEach((opt) => {
      const o = document.createElement('option');
      o.value = opt;
      o.textContent = opt.replace('_', ' ');
      if (step.status === opt) o.selected = true;
      status.appendChild(o);
    });
    status.addEventListener('change', () => updateSetupStep(step.id, status.value));
    row.appendChild(title);
    row.appendChild(notes);
    row.appendChild(status);
    if (step.id === 'program_scopes') {
      const meta = document.createElement('div');
      meta.className = 'setup-notes';
      const last = programStatus && programStatus.last_sync ? programStatus.last_sync : 'never';
      const state = programStatus && programStatus.status ? programStatus.status : 'unknown';
      meta.textContent = `last sync: ${last} · status: ${state}`;
      const btn = document.createElement('button');
      btn.className = 'setup-sync';
      btn.textContent = 'Sync now';
      btn.addEventListener('click', () => triggerProgramSync());
      row.appendChild(meta);
      row.appendChild(btn);
    }
    el.appendChild(row);
  });
}

async function loadKeyCatalog() {
  const el = document.getElementById('keyCatalog');
  if (!el) return;
  try {
    const res = await fetch('/api/keys/catalog');
    const data = await res.json();
    renderKeyCatalog(el, data.catalog || []);
  } catch (e) {
    el.textContent = 'Failed to load API key catalog.';
  }
}

function renderKeyCatalog(el, items) {
  el.innerHTML = '';
  if (!items.length) {
    el.textContent = 'No API keys configured.';
    return;
  }
  items.forEach((item) => {
    const row = document.createElement('div');
    row.className = 'key-row';
    const name = document.createElement('div');
    name.className = 'key-name';
    name.textContent = `${item.name} · ${item.category}`;
    const notes = document.createElement('div');
    notes.className = 'key-notes';
    notes.textContent = item.notes || '';
    const meta = document.createElement('div');
    meta.className = 'key-meta';
    meta.textContent = `vault: ${item.vault_source_id || 'source.unknown'} · scopes: ${(item.scopes || []).join(', ')}`;
    const link = document.createElement('a');
    link.className = 'key-link';
    link.href = item.url || '#';
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = 'Get Key';
    row.appendChild(name);
    row.appendChild(notes);
    row.appendChild(meta);
    row.appendChild(link);
    el.appendChild(row);
  });
}

window.addEventListener('load', () => {
  loadSetupHub();
  loadKeyCatalog();
});
