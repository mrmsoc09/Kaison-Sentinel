async function queueEmail() {
  const out = document.getElementById('emailStatus');
  const runId = document.getElementById('emailRunId').value.trim();
  const to = document.getElementById('emailTo').value.split(',').map(s => s.trim()).filter(Boolean);
  const subject = document.getElementById('emailSubject').value.trim();
  const body = document.getElementById('emailBody').value;
  const hil = document.getElementById('emailHilConfirm')?.checked;
  const htmlBody = window._emailHtml || '';
  const attachments = window._emailAttachments || [];
  try {
    const res = await fetch('/api/notify/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ run_id: runId, to, subject, body, html_body: htmlBody, attachments, hil_confirmed: hil })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Email queue error.';
  }
}

async function draftEmail() {
  const out = document.getElementById('emailStatus');
  const runId = document.getElementById('emailRunId').value.trim();
  const to = document.getElementById('emailTo').value.split(',').map(s => s.trim()).filter(Boolean);
  const subject = document.getElementById('emailSubject').value.trim();
  try {
    const res = await fetch('/api/email/draft', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ run_id: runId, to, subject })
    });
    const data = await res.json();
    if (data.body) document.getElementById('emailBody').value = data.body;
    window._emailHtml = data.html_body || '';
    window._emailAttachments = data.attachments || [];
    out.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    out.textContent = 'Email draft error.';
  }
}

window.addEventListener('load', () => {
  const btn = document.getElementById('emailQueueBtn');
  if (btn) btn.addEventListener('click', queueEmail);
  const draftBtn = document.getElementById('emailDraftBtn');
  if (draftBtn) draftBtn.addEventListener('click', draftEmail);
});
