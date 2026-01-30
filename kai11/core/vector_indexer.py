from pathlib import Path
from typing import Dict, Any

from ..vector.store_factory import get_store
from .config import OUTPUT_DIR

VEC_PATH = OUTPUT_DIR / "vector_store.jsonl"


def append_vector(event: Dict[str, Any]) -> None:
    store = get_store(VEC_PATH)
    text = str(event.get('value'))
    doc_id = f"{event.get('module')}:{event.get('tool')}:{event.get('type')}"
    store.add(doc_id=doc_id, path=event.get('target',''), chunk_id=0, text=text)
    store.save(VEC_PATH)
