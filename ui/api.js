const API_KEY_STORAGE = 'kaison_api_key';
const API_HEADER = 'X-API-Key';

function getApiKey() {
  return localStorage.getItem(API_KEY_STORAGE) || '';
}

function setApiKey(val) {
  if (val) {
    localStorage.setItem(API_KEY_STORAGE, val);
  } else {
    localStorage.removeItem(API_KEY_STORAGE);
  }
}

function initApiKeyUI() {
  const input = document.getElementById('apiKeyInput');
  const status = document.getElementById('apiKeyStatus');
  if (!input) return;
  input.value = getApiKey();
  const save = document.getElementById('apiKeySave');
  const clear = document.getElementById('apiKeyClear');
  if (save) save.addEventListener('click', () => {
    setApiKey(input.value.trim());
    if (status) status.textContent = 'API key saved locally.';
  });
  if (clear) clear.addEventListener('click', () => {
    setApiKey('');
    input.value = '';
    if (status) status.textContent = 'API key cleared.';
  });
}

const _fetch = window.fetch.bind(window);
window.fetch = (url, options = {}) => {
  try {
    if (typeof url === 'string' && url.startsWith('/api/')) {
      const key = getApiKey();
      if (key) {
        options.headers = Object.assign({}, options.headers || {}, { [API_HEADER]: key });
      }
    }
  } catch (e) {
    // ignore
  }
  return _fetch(url, options);
};

window.addEventListener('load', initApiKeyUI);
