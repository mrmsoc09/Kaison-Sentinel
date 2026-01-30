async function loadMitreTechniques() {
  const sel = document.getElementById('mitreTechnique');
  if (!sel) return;
  try {
    const res = await fetch('/api/mitre/techniques');
    const data = await res.json();
    const list = data.techniques || [];
    sel.innerHTML = '';
    list.forEach((t) => {
      const opt = document.createElement('option');
      opt.value = t.technique_id;
      opt.textContent = `${t.technique_id} · ${t.technique}`;
      sel.appendChild(opt);
    });
  } catch (e) {
    // ignore
  }
}

function mitreScopePayload() {
  const allowlist = document.getElementById('mitreAllowlist')?.value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
  return { allowlist: allowlist || [] };
}

async function generateMitrePlan() {
  const out = document.getElementById('mitreOut');
  const sel = document.getElementById('mitreTechnique');
  if (!out || !sel) return;
  const technique = sel.value.trim();
  const hil = document.getElementById('mitreHil')?.checked;
  if (!technique) {
    out.textContent = 'Select a technique.';
    return;
  }
  out.textContent = 'Generating...';
  try {
    const res = await fetch('/api/mitre/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        technique_id: technique,
        hil_approved: Boolean(hil),
        scope: mitreScopePayload()
      })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
    if (data.status === 'ok') {
      applyMitreToPlan(data);
    }
  } catch (e) {
    out.textContent = 'MITRE plan error.';
  }
}

async function exportMitreBundle() {
  const out = document.getElementById('mitreOut');
  const sel = document.getElementById('mitreTechnique');
  if (!out || !sel) return;
  const technique = sel.value.trim();
  const hil = document.getElementById('mitreHil')?.checked;
  if (!technique) {
    out.textContent = 'Select a technique.';
    return;
  }
  out.textContent = 'Exporting bundle...';
  try {
    const res = await fetch('/api/mitre/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        technique_id: technique,
        hil_approved: Boolean(hil),
        scope: mitreScopePayload()
      })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
    if (data.status === 'ok') {
      applyMitreToPlan(data);
    }
  } catch (e) {
    out.textContent = 'MITRE export error.';
  }
}

function applyMitreToPlan(data) {
  const playbooks = data.recommended_playbooks || [];
  const planPlaybooks = document.getElementById('planPlaybooks');
  if (planPlaybooks) {
    planPlaybooks.value = playbooks.join(', ');
  }
  const planMitre = document.getElementById('planMitre');
  if (planMitre) {
    planMitre.value = data.technique_id || '';
  }
  const planKind = document.getElementById('planKind');
  if (planKind) {
    const hasOsint = playbooks.some(p => p.includes('osint'));
    const hasVuln = playbooks.some(p => p.includes('vuln'));
    if (hasOsint && hasVuln) planKind.value = 'all';
    else if (hasVuln) planKind.value = 'vuln';
    else if (hasOsint) planKind.value = 'osint';
  }
}

window.addEventListener('load', loadMitreTechniques);
const mitreBtn = document.getElementById('mitrePlanBtn');
if (mitreBtn) mitreBtn.addEventListener('click', generateMitrePlan);
const mitreExportBtn = document.getElementById('mitreExportBtn');
if (mitreExportBtn) mitreExportBtn.addEventListener('click', exportMitreBundle);
