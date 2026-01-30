import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .embed import embed_text, cosine_sparse
from ..core.config import TOP_K_DEFAULT


class VectorStore:
    def __init__(self):
        self.rows: List[dict] = []

    def add(self, *, doc_id: str, path: str, chunk_id: int, text: str, meta: Optional[dict] = None) -> None:
        vec = embed_text(text)
        self.rows.append({
            "id": doc_id,
            "path": path,
            "chunk_id": chunk_id,
            "text": text,
            "vector": vec,
            "meta": meta or {},
        })

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for row in self.rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    @classmethod
    def load(cls, path: Path) -> "VectorStore":
        store = cls()
        if not path.exists():
            return store
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    store.rows.append(json.loads(line))
                except Exception:
                    continue
        return store

    def search(self, query: str, top_k: int = TOP_K_DEFAULT) -> List[dict]:
        qv = embed_text(query)
        scored: List[Tuple[float, dict]] = []
        for row in self.rows:
            score = cosine_sparse(qv, row.get("vector", {}))
            if score > 0:
                scored.append((score, row))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, row in scored[: max(1, top_k)]:
            results.append({
                "score": round(score, 4),
                "id": row.get("id"),
                "path": row.get("path"),
                "chunk_id": row.get("chunk_id"),
                "text": row.get("text"),
                "meta": row.get("meta", {}),
            })
        return results
