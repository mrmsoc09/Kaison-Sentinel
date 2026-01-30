async function loadAssets(endpoint, targetId) {
  try {
    const res = await fetch(endpoint);
    const data = await res.json();
    const el = document.getElementById(targetId);
    if (!el) return;
    el.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    const el = document.getElementById(targetId);
    if (el) el.textContent = 'Failed to load assets.';
  }
}

window.addEventListener('load', () => {
  loadAssets('/api/assets/prompts', 'assetPrompts');
  loadAssets('/api/assets/personas', 'assetPersonas');
  loadAssets('/api/assets/personas_praison', 'assetPersonasPraison');
  loadAssets('/api/assets/personas_langstudio', 'assetPersonasLang');
  loadAssets('/api/assets/playbooks', 'assetPlaybooks');
  loadAssets('/api/assets/report_formats', 'assetReports');
  loadAssets('/api/assets/agents', 'assetAgents');
  loadAssets('/api/options', 'assetOptions');
  loadAssets('/api/options?kind=osint', 'assetOptionsOsint');
  loadAssets('/api/options?kind=vuln', 'assetOptionsVuln');
  loadAssets('/api/options?kind=validation', 'assetOptionsValidation');
  loadAssets('/api/tools/health', 'assetHealth');
  loadAssets('/api/tools/registry', 'assetToolRegistry');
  loadAssets('/api/tools/osint', 'assetToolsOsint');
  loadAssets('/api/tools/vuln', 'assetToolsVuln');
  loadAssets('/api/tools/substitutes', 'assetToolSubs');
});
