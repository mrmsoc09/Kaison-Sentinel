import os
from pathlib import Path
from typing import Optional

from .vector_store import VectorStore


def get_store(path: Optional[Path] = None):
    backend = os.getenv("KAI_VECTOR_BACKEND", "file").lower()
    if backend == "pgvector":
        try:
            from .pgvector_store import PgVectorStore
            return PgVectorStore.from_env()
        except Exception:
            # Fall back to file store if pgvector not available
            return VectorStore.load(path) if path else VectorStore()
    return VectorStore.load(path) if path else VectorStore()
