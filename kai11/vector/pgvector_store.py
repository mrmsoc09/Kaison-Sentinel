import os
import json
from typing import List, Optional

from .embed import embed_text, sparse_to_dense
from ..core.config import EMBED_DIM
from ..core.options import get_options
from ..core.vault import get_key


class PgVectorStore:
    def __init__(self, dsn: str):
        import psycopg
        self._psycopg = psycopg
        self._dsn = dsn
        self._ensure_schema()

    @classmethod
    def from_env(cls) -> "PgVectorStore":
        dsn = os.getenv("KAI_PGVECTOR_DSN")
        if not dsn:
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
            dsn = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        return cls(dsn)

    def _ensure_schema(self) -> None:
        with self._psycopg.connect(self._dsn) as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS kai_vectors (
                    id TEXT PRIMARY KEY,
                    path TEXT,
                    chunk_id INT,
                    text TEXT,
                    meta JSONB,
                    embedding VECTOR(%s)
                )
                """,
                (EMBED_DIM,),
            )
            conn.commit()

    def add(self, *, doc_id: str, path: str, chunk_id: int, text: str, meta: Optional[dict] = None) -> None:
        vec = sparse_to_dense(embed_text(text), EMBED_DIM)
        meta_json = json.dumps(meta or {})
        with self._psycopg.connect(self._dsn) as conn:
            conn.execute(
                """
                INSERT INTO kai_vectors (id, path, chunk_id, text, meta, embedding)
                VALUES (%s, %s, %s, %s, %s::jsonb, %s)
                ON CONFLICT (id) DO UPDATE SET
                    path = EXCLUDED.path,
                    chunk_id = EXCLUDED.chunk_id,
                    text = EXCLUDED.text,
                    meta = EXCLUDED.meta,
                    embedding = EXCLUDED.embedding
                """,
                (doc_id, path, chunk_id, text, meta_json, vec),
            )
            conn.commit()

    def save(self, _path=None) -> None:
        # No-op for pgvector; writes are immediate.
        return None

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        qv = sparse_to_dense(embed_text(query), EMBED_DIM)
        with self._psycopg.connect(self._dsn) as conn:
            rows = conn.execute(
                """
                SELECT id, path, chunk_id, text, meta, 1 - (embedding <=> %s) AS score
                FROM kai_vectors
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (qv, qv, top_k),
            ).fetchall()
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "path": row[1],
                "chunk_id": row[2],
                "text": row[3],
                "meta": row[4] or {},
                "score": round(float(row[5]), 4),
            })
        return results
