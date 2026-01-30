import os
import re
import subprocess
from pathlib import Path
from typing import Iterable, Iterator, List, Tuple

from ..core.config import ROOT, SKIP_DIRS, TEXT_EXTS, PDF_EXTS, MAX_FILE_BYTES, CHUNK_TARGET_CHARS, CHUNK_MIN_CHARS, CHUNK_OVERLAP_CHARS


def _is_skipped_dir(path: Path) -> bool:
    return path.name in SKIP_DIRS


def iter_files(root: Path = ROOT) -> Iterator[Path]:
    for base, dirs, files in os.walk(root):
        base_path = Path(base)
        # prune skip dirs
        dirs[:] = [d for d in dirs if not _is_skipped_dir(base_path / d)]
        for f in files:
            p = base_path / f
            ext = p.suffix.lower()
            if ext in TEXT_EXTS or ext in PDF_EXTS:
                yield p


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(path: Path) -> str:
    # Use pdftotext (already installed on this system)
    tmp_out = Path("/tmp") / (path.stem + "_kai11.txt")
    try:
        subprocess.run([
            "pdftotext",
            "-layout",
            str(path),
            str(tmp_out),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return tmp_out.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    finally:
        try:
            if tmp_out.exists():
                tmp_out.unlink()
        except Exception:
            pass


def read_text(path: Path) -> str:
    if path.suffix.lower() in PDF_EXTS:
        return _read_pdf(path)
    return _read_text_file(path)


def _normalize(text: str) -> str:
    # collapse repeated whitespace
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, target: int = CHUNK_TARGET_CHARS, overlap: int = CHUNK_OVERLAP_CHARS) -> List[str]:
    text = _normalize(text)
    if not text:
        return []
    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + target)
        chunk = text[start:end].strip()
        if len(chunk) >= CHUNK_MIN_CHARS:
            chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks


def ingest_documents(root: Path = ROOT) -> Iterator[Tuple[Path, List[str]]]:
    for path in iter_files(root):
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except Exception:
            continue
        text = read_text(path)
        if not text:
            continue
        chunks = chunk_text(text)
        if chunks:
            yield path, chunks
