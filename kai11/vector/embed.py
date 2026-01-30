import math
import re
import hashlib
from typing import Dict, Iterable

from ..core.config import EMBED_DIM

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def _tokenize(text: str) -> Iterable[str]:
    for tok in TOKEN_RE.findall(text.lower()):
        if tok:
            yield tok


def _hash_token(token: str) -> int:
    h = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return int(h[:16], 16) % EMBED_DIM


def embed_text(text: str) -> Dict[int, float]:
    counts: Dict[int, float] = {}
    for tok in _tokenize(text):
        idx = _hash_token(tok)
        counts[idx] = counts.get(idx, 0.0) + 1.0
    # L2 normalize
    norm = math.sqrt(sum(v * v for v in counts.values())) or 1.0
    return {k: v / norm for k, v in counts.items()}


def cosine_sparse(a: Dict[int, float], b: Dict[int, float]) -> float:
    if not a or not b:
        return 0.0
    # iterate smaller map
    if len(a) > len(b):
        a, b = b, a
    dot = 0.0
    for k, v in a.items():
        bv = b.get(k)
        if bv is not None:
            dot += v * bv
    return dot


def sparse_to_dense(vec: Dict[int, float], dim: int = EMBED_DIM) -> list[float]:
    dense = [0.0] * dim
    for k, v in vec.items():
        if 0 <= k < dim:
            dense[k] = float(v)
    return dense
