async function loadProxyOverrides() {
  const out = document.getElementById('proxyStatus');
  try {
    const res = await fetch('/api/options/override');
    const data = await res.json();
    const proxy = data.proxy || {};
    const http = document.getElementById('proxyHttp');
    const https = document.getElementById('proxyHttps');
    const no = document.getElementById('proxyNo');
    if (http) http.value = proxy.http || '';
    if (https) https.value = proxy.https || '';
    if (no) no.value = proxy.no_proxy || '';
    if (out) out.textContent = 'Loaded.';
  } catch (e) {
    if (out) out.textContent = 'Failed to load proxy overrides.';
  }
}

async function saveProxyOverrides() {
  const out = document.getElementById('proxyStatus');
  const payload = {
    proxy: {
      http: document.getElementById('proxyHttp').value.trim(),
      https: document.getElementById('proxyHttps').value.trim(),
      no_proxy: document.getElementById('proxyNo').value.trim(),
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
    if (out) out.textContent = 'Proxy save error.';
  }
}

window.addEventListener('load', () => {
  loadProxyOverrides();
  const btn = document.getElementById('proxySave');
  if (btn) btn.addEventListener('click', saveProxyOverrides);
});
