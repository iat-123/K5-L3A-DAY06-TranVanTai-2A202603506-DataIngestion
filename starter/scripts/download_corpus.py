"""Download the corpus PDF listed in corpus.json and verify its SHA-256.

Run from starter/:  python scripts/download_corpus.py
The PDF is not committed (see .gitignore); this script recreates it.
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "corpus.json").read_text(encoding="utf-8"))
target = ROOT / config["local_path"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


if not target.exists():
    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {config['source_url']}")
    urllib.request.urlretrieve(config["source_url"], target)

actual = sha256(target)
if actual != config["sha256"]:
    sys.exit(f"SHA-256 mismatch for {target}: got {actual}, expected {config['sha256']}. "
             "OpenStax may have published a new version; re-check pages and benchmark before use.")
print(f"OK {target} sha256={actual}")
