from pathlib import Path

ROOT = Path("/home/user23/KAI")
BUILD_ROOT = Path("/home/user23/KAI/builds/Kai 1.1")
OUTPUT_DIR = BUILD_ROOT / "outputs"
RUNS_DIR = OUTPUT_DIR / "runs"
REPORTS_DIR = OUTPUT_DIR / "reports"
LOGS_DIR = OUTPUT_DIR / "logs"
EVIDENCE_DIR = OUTPUT_DIR / "evidence"
TRACE_DIR = OUTPUT_DIR / "traces"
LANGSTUDIO_DIR = OUTPUT_DIR / "langstudio"
LOOPS_DIR = OUTPUT_DIR / "loops"

# Ingestion settings
MAX_FILE_BYTES = 25 * 1024 * 1024  # 25 MB
CHUNK_TARGET_CHARS = 1200
CHUNK_MIN_CHARS = 400
CHUNK_OVERLAP_CHARS = 120

# Vector store settings
EMBED_DIM = 2048
TOP_K_DEFAULT = 5

# Directories to skip during ingestion
SKIP_DIRS = {
    ".git", ".cache", "node_modules", "__pycache__", ".venv", ".idea", ".vscode",
    "builds", "outputs", "dist", "tmp", "logs", "artifacts",
}

# File extensions to ingest
TEXT_EXTS = {
    ".md", ".txt", ".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml",
    ".ini", ".cfg", ".csv", ".rst", ".sql",
}

PDF_EXTS = {".pdf"}
