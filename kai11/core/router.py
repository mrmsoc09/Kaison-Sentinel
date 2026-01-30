from typing import Dict, Any

from .training import append_training
from .vector_indexer import append_vector
from .knowledge_store import append_knowledge


def route_artifact(event: Dict[str, Any]) -> None:
    # Always send to training + vector for now
    append_training(event)
    append_vector(event)
    append_knowledge(event)
