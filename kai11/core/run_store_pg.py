import os
from datetime import datetime
from typing import Dict, Any

from .options import get_options
from .vault import get_key


def _dsn() -> str:
    dsn = os.getenv("KAI_PGVECTOR_DSN")
    if dsn:
        return dsn
    opts = get_options("all")
    db_cfg = opts.get("db", {})
    host = os.getenv("KAI_PG_HOST", db_cfg.get("host", "localhost"))
    port = os.getenv("KAI_PG_PORT", db_cfg.get("port", "5432"))
    db = os.getenv("KAI_PG_DB", db_cfg.get("name", "kaison"))
    user = os.getenv("KAI_PG_USER", db_cfg.get("user", "kaison"))
    password = os.getenv("KAI_PG_PASSWORD")
    if not password:
        source = db_cfg.get("password_source")
        if source:
            res = get_key(source)
            if res.get("status") == "ok":
                password = res.get("key")
    password = password or "kaison"
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def store_run_metadata(record: Dict[str, Any]) -> Dict[str, Any]:
    try:
        import psycopg
    except Exception as e:
        return {"status": "error", "reason": f"psycopg_missing: {e}"}

    dsn = _dsn()
    with psycopg.connect(dsn) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kai_runs (
                run_id TEXT PRIMARY KEY,
                tenant_id TEXT,
                mode TEXT,
                created_at TEXT,
                findings_count INT,
                report_bundle JSONB
            )
            """
        )
        conn.execute(
            """
            INSERT INTO kai_runs (run_id, tenant_id, mode, created_at, findings_count, report_bundle)
            VALUES (%s, %s, %s, %s, %s, %s::jsonb)
            ON CONFLICT (run_id) DO UPDATE SET
                tenant_id = EXCLUDED.tenant_id,
                mode = EXCLUDED.mode,
                findings_count = EXCLUDED.findings_count,
                report_bundle = EXCLUDED.report_bundle
            """,
            (
                record.get("run_id"),
                record.get("tenant_id", ""),
                record.get("mode"),
                record.get("created_at") or datetime.utcnow().isoformat(),
                record.get("findings_count", 0),
                record.get("report_bundle") or {},
            ),
        )
        conn.commit()
    return {"status": "ok"}
