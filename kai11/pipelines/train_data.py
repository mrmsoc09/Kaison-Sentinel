import re
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Tuple


def _keywords(text: str, top_n: int = 8) -> List[str]:
    words = re.findall(r"[A-Za-z0-9_]+", text.lower())
    stop = {
        "the","and","for","with","this","that","from","into","your","you","are","was","were",
        "not","but","can","will","use","using","should","must","may","any","all","our","their",
        "data","system","model","agent","tool","tools","scan","scans","security","vulnerability",
    }
    freq: Dict[str, int] = {}
    for w in words:
        if len(w) < 3 or w in stop:
            continue
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in ranked[:top_n]]


def _title_from_path(path: Path) -> str:
    return path.name


def generate_training_rows(path: Path, chunk: str, chunk_id: int) -> List[dict]:
    title = _title_from_path(path)
    keys = _keywords(chunk)
    rows: List[dict] = []
    rows.append({
        "prompt": f"Summarize this passage from {title}:",
        "response": chunk[:800].strip(),
        "type": "summary",
    })
    if keys:
        rows.append({
            "prompt": f"List key topics in this section of {title}:",
            "response": ", ".join(keys),
            "type": "keywords",
        })
    # lightweight Q/A style
    rows.append({
        "prompt": f"What is the main idea described in {title} (chunk {chunk_id})?",
        "response": chunk[:600].strip(),
        "type": "qa",
    })
    return rows
