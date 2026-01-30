async function loadProfile() {
  try {
    const res = await fetch('/api/profile');
    const data = await res.json();
    document.getElementById('profileName').value = data.name || '';
    document.getElementById('profileOrg').value = data.org || '';
    document.getElementById('profileEmail').value = data.email || '';
  } catch (e) {
    // ignore
  }
}

async function saveProfile() {
  const payload = {
    name: document.getElementById('profileName').value.trim(),
    org: document.getElementById('profileOrg').value.trim(),
    email: document.getElementById('profileEmail').value.trim(),
  };
  const out = document.getElementById('emailStatus');
  try {
    const res = await fetch('/api/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Profile save error.';
  }
}

async function loadEmailConfig() {
  try {
    const res = await fetch('/api/email/config');
    const data = await res.json();
    document.getElementById('emailProvider').value = data.provider || 'gmail_smtp';
    document.getElementById('emailFrom').value = data.from_email || '';
    document.getElementById('emailUser').value = data.username || '';
    document.getElementById('emailHost').value = data.smtp_host || '';
    document.getElementById('emailPort').value = data.smtp_port || '';
    document.getElementById('emailPasswordSource').value = data.password_source_id || '';
    document.getElementById('emailStarttls').checked = !!data.use_starttls;
    document.getElementById('emailSsl').checked = !!data.use_ssl;
    document.getElementById('emailEnabled').checked = !!data.enabled;
    applyEmailProviderHints();
  } catch (e) {
    // ignore
  }
}

async function saveEmailConfig() {
  const payload = {
    provider: document.getElementById('emailProvider').value,
    from_email: document.getElementById('emailFrom').value.trim(),
    username: document.getElementById('emailUser').value.trim(),
    smtp_host: document.getElementById('emailHost').value.trim(),
    smtp_port: parseInt(document.getElementById('emailPort').value || '0', 10),
    password_source_id: document.getElementById('emailPasswordSource').value.trim(),
    use_starttls: document.getElementById('emailStarttls').checked,
    use_ssl: document.getElementById('emailSsl').checked,
    enabled: document.getElementById('emailEnabled').checked,
  };
  const out = document.getElementById('emailStatus');
  try {
    const res = await fetch('/api/email/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Email config save error.';
  }
}

function applyEmailProviderHints() {
  const provider = document.getElementById('emailProvider').value;
  const hostEl = document.getElementById('emailHost');
  const portEl = document.getElementById('emailPort');
  const helpEl = document.getElementById('emailProviderHelp');
  if (!helpEl) return;
  if (provider === 'gmail_smtp') {
    hostEl.placeholder = 'smtp.gmail.com';
    portEl.placeholder = '587';
    helpEl.textContent = 'Gmail SMTP: use an app password; common settings are smtp.gmail.com:587 with STARTTLS.';
  } else if (provider === 'proton_bridge') {
    hostEl.placeholder = 'Use Proton Bridge host';
    portEl.placeholder = 'Use Proton Bridge port';
    helpEl.textContent = 'Proton Mail Bridge: use the local SMTP host/port shown in the Bridge app (no direct SMTP without Bridge).';
  } else {
    hostEl.placeholder = 'SMTP host';
    portEl.placeholder = 'SMTP port';
    helpEl.textContent = 'Custom SMTP: enter your provider host/port and security settings.';
  }
}

window.addEventListener('load', () => {
  loadProfile();
  loadEmailConfig();
  const providerSelect = document.getElementById('emailProvider');
  if (providerSelect) providerSelect.addEventListener('change', applyEmailProviderHints);
  const saveProfileBtn = document.getElementById('profileSaveBtn');
  if (saveProfileBtn) saveProfileBtn.addEventListener('click', saveProfile);
  const saveEmailBtn = document.getElementById('emailConfigSaveBtn');
  if (saveEmailBtn) saveEmailBtn.addEventListener('click', saveEmailConfig);
});
