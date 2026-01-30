async function doExecute() {
  const out = document.getElementById('executeOut');
  const goal = document.getElementById('planGoal').value.trim();
  const targets = document.getElementById('planTargets').value.split(',').map(s => s.trim()).filter(Boolean);
  const constraints = document.getElementById('planConstraints').value.trim();
  const playbooks = document.getElementById('planPlaybooks')?.value
    .split(',')
    .map(s => s.trim())
    .filter(Boolean);
  const mitreId = document.getElementById('planMitre')?.value.trim();
  const budgetTier = document.getElementById('planBudgetTier')?.value;
  const dailyBudget = parseFloat(document.getElementById('planBudgetDaily')?.value || '');
  const stealth = document.getElementById('planStealth')?.value;
  const durationDays = parseInt(document.getElementById('planDuration')?.value || '', 10);
  const poolSize = parseInt(document.getElementById('planPoolSize')?.value || '', 10);
  const activeLimit = parseInt(document.getElementById('planActiveLimit')?.value || '', 10);
  const autoInstall = document.getElementById('planAutoInstall')?.checked;
  const kind = document.getElementById('planKind').value;
  const role = document.getElementById('planRole').value;
  const approve = document.getElementById('executeApprove').checked;
  const validationConfirmed = document.getElementById('validationConfirm')?.checked;
  const reportHilConfirmed = document.getElementById('reportHilConfirm')?.checked;
  const tier = document.getElementById('mitigationTier').value;
  const reportFormat = document.getElementById('reportFormat')?.value;
  out.textContent = 'Executing...';
  try {
    const res = await fetch('/api/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        approve: approve,
        mitigation_tier: tier,
        scope: {
          allowlist: targets,
          goal: goal,
          constraints: constraints,
          playbook_ids: playbooks || [],
          mitre_technique_id: mitreId || undefined,
          budget_tier: budgetTier || undefined,
          daily_budget_usd: Number.isFinite(dailyBudget) ? dailyBudget : undefined,
          stealth: stealth || undefined,
          scan_duration_days: Number.isFinite(durationDays) ? durationDays : undefined,
          scan_pool_size: Number.isFinite(poolSize) ? poolSize : undefined,
          max_active_scans: Number.isFinite(activeLimit) ? activeLimit : undefined,
          auto_install_tools: !!autoInstall,
          allow_install: !!autoInstall,
          module_kind: kind,
          role: role,
          validation_confirmed: validationConfirmed,
          report_hil_confirmed: reportHilConfirmed,
          report_format_id: reportFormat || undefined
        }
      })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Execute error.';
  }
}

window.addEventListener('load', () => {
  const btn = document.getElementById('executeBtn');
  if (btn) btn.addEventListener('click', doExecute);
});
