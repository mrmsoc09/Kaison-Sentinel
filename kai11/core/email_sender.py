import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, Any

from .email_config import load_email_config
from .vault import get_key


def send_email(payload: Dict[str, Any]) -> Dict[str, Any]:
    cfg = load_email_config()
    if not cfg.get("enabled", False):
        return {"status": "disabled"}

    from_email = cfg.get("from_email") or cfg.get("username")
    to = payload.get("to") or []
    if isinstance(to, str):
        to = [t.strip() for t in to.split(",") if t.strip()]
    subject = payload.get("subject", "")
    body = payload.get("body", "")
    html_body = payload.get("html_body", "")
    attachments = payload.get("attachments") or []

    if not from_email or not to:
        return {"status": "error", "reason": "from_or_to_missing"}

    password = None
    source_id = cfg.get("password_source_id")
    if source_id:
        key = get_key(source_id)
        if key.get("status") == "ok":
            password = key.get("key")

    host = cfg.get("smtp_host")
    port = int(cfg.get("smtp_port") or 587)
    use_ssl = bool(cfg.get("use_ssl"))
    use_starttls = bool(cfg.get("use_starttls"))

    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    for path in attachments:
        try:
            p = Path(path)
            if not p.exists():
                continue
            if p.suffix == ".enc":
                continue
            data = p.read_bytes()
            if p.suffix == ".html":
                maintype, subtype = "text", "html"
            elif p.suffix == ".json":
                maintype, subtype = "application", "json"
            elif p.suffix == ".csv":
                maintype, subtype = "text", "csv"
            elif p.suffix == ".sarif":
                maintype, subtype = "application", "json"
            elif p.suffix == ".pdf":
                maintype, subtype = "application", "pdf"
            else:
                maintype, subtype = "application", "octet-stream"
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=p.name)
        except Exception:
            continue

    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(host, port, timeout=15)
        else:
            server = smtplib.SMTP(host, port, timeout=15)
        if use_starttls and not use_ssl:
            server.starttls()
        if cfg.get("username") and password:
            server.login(cfg.get("username"), password)
        server.send_message(msg)
        server.quit()
        return {"status": "sent", "provider": cfg.get("provider")}
    except Exception as e:
        return {"status": "error", "reason": str(e)}
