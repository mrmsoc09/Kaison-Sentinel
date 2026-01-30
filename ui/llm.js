async function loadLlmProviders() {
  const el = document.getElementById('llmProviders');
  if (!el) return;
  try {
    const res = await fetch('/api/llm/providers');
    const data = await res.json();
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    el.textContent = 'LLM providers unavailable.';
  }
}

window.addEventListener('load', loadLlmProviders);
