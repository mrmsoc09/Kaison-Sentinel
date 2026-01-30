import argparse
import json
from pathlib import Path
from typing import Dict

from ..core.config import ROOT, OUTPUT_DIR
from .ingest import ingest_documents
from ..vector.store_factory import get_store
from .train_data import generate_training_rows


def run_pipeline(source: Path, out_dir: Path) -> Dict[str, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    vector_path = out_dir / "vector_store.jsonl"
    train_path = out_dir / "training_data.jsonl"
    stats_path = out_dir / "stats.json"

    store = get_store(vector_path)
    total_docs = 0
    total_chunks = 0
    total_rows = 0

    with train_path.open("w", encoding="utf-8") as tf:
        for path, chunks in ingest_documents(source):
            total_docs += 1
            for i, chunk in enumerate(chunks):
                total_chunks += 1
                doc_id = f"{path.name}:{i}"
                store.add(doc_id=doc_id, path=str(path), chunk_id=i, text=chunk)
                rows = generate_training_rows(path, chunk, i)
                for row in rows:
                    total_rows += 1
                    record = {
                        "id": f"{doc_id}:{row.get('type')}",
                        "source_path": str(path),
                        "chunk_id": i,
                        "prompt": row["prompt"],
                        "response": row["response"],
                        "type": row.get("type"),
                    }
                    tf.write(json.dumps(record, ensure_ascii=False) + "\n")

    store.save(vector_path)

    stats = {
        "documents_ingested": total_docs,
        "chunks_indexed": total_chunks,
        "training_rows": total_rows,
        "vector_store": str(vector_path),
        "training_data": str(train_path),
    }
    stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(ROOT))
    parser.add_argument("--out", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    stats = run_pipeline(Path(args.source), Path(args.out))
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
