async function loadPlatformOptions() {
  const out = document.getElementById('platformOptionsStatus');
  try {
    const res = await fetch('/api/options/override');
    const data = await res.json();
    const shared = data || {};
    document.getElementById('optVaultBackend').value = shared.vault_backend || 'local';
    document.getElementById('optLlmProvider').value = shared.llm_active_provider || '';
    const db = shared.db || {};
    document.getElementById('optDbHost').value = db.host || '';
    document.getElementById('optDbPort').value = db.port || '';
    document.getElementById('optDbName').value = db.name || '';
    document.getElementById('optDbUser').value = db.user || '';
    document.getElementById('optDbPassSource').value = db.password_source || '';
    document.getElementById('optDbSsl').value = db.sslmode || '';
    document.getElementById('optAutoInstall').checked = !!shared.auto_install_tools;
    document.getElementById('optAllowInstall').checked = !!shared.allow_install;
    const ps = shared.program_sync || {};
    document.getElementById('optProgramSync').checked = !!ps.enabled;
    document.getElementById('optProgramAuto').checked = !!ps.auto_trigger;
    document.getElementById('optProgramInterval').value = ps.interval_hours || '';
    if (out) out.textContent = 'Loaded.';
  } catch (e) {
    if (out) out.textContent = 'Options load error.';
  }
}

async function savePlatformOptions() {
  const out = document.getElementById('platformOptionsStatus');
  const payload = {
    vault_backend: document.getElementById('optVaultBackend').value,
    llm_active_provider: document.getElementById('optLlmProvider').value,
    db: {
      host: document.getElementById('optDbHost').value.trim(),
      port: document.getElementById('optDbPort').value.trim(),
      name: document.getElementById('optDbName').value.trim(),
      user: document.getElementById('optDbUser').value.trim(),
      password_source: document.getElementById('optDbPassSource').value.trim(),
      sslmode: document.getElementById('optDbSsl').value.trim()
    },
    auto_install_tools: document.getElementById('optAutoInstall').checked,
    allow_install: document.getElementById('optAllowInstall').checked,
    program_sync: {
      enabled: document.getElementById('optProgramSync').checked,
      auto_trigger: document.getElementById('optProgramAuto').checked,
      interval_hours: parseFloat(document.getElementById('optProgramInterval').value || '') || 24
    }
  };
  try {
    const res = await fetch('/api/options/override', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (out) out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    if (out) out.textContent = 'Options save error.';
  }
}

window.addEventListener('load', () => {
  loadPlatformOptions();
  const btn = document.getElementById('platformOptionsSave');
  if (btn) btn.addEventListener('click', savePlatformOptions);
});
