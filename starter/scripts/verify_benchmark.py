"""Verify every benchmark evidence quote exists on its gold page (after normalization).

Run from starter/:  python scripts/verify_benchmark.py
Checks: quote found on gold page (whitespace-insensitive), gold page is a counted
content page, filter value matches the gold page's chapter, split counts.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.ingestion import load_pdf  # noqa: E402

config = json.loads((ROOT / "corpus.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT.parent / "data" / "manifest.json").read_text(encoding="utf-8"))
page_info = {p["pdf_page"]: p for p in manifest["pages"]}
pages = {p.page: p for c in config["chapters"]
         for p in load_pdf(ROOT / config["local_path"], config["source_id"], config["local_path"],
                           c["pdf_first_page"], c["pdf_last_page"])}


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


questions = [json.loads(line) for line in
             (ROOT.parent / "benchmark" / "questions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
errors = []
for q in questions:
    golds = [{"gold_page": q["gold_page"], "evidence_quote": q["evidence_quote"]}] + q.get("alternatives", [])
    for gold in golds:
        page = gold["gold_page"]
        if page not in pages or not page_info[page]["counted"]:
            errors.append(f"{q['id']}: gold page {page} is not a counted content page")
            continue
        if squash(gold["evidence_quote"]) not in squash(pages[page].text):
            errors.append(f"{q['id']}: evidence not found on page {page}")
        if q.get("filter") and q["filter"].get("chapter") != page_info[page]["chapter"]:
            errors.append(f"{q['id']}: filter {q['filter']} does not match page {page} chapter")

ids = [q["id"] for q in questions]
splits = Counter(q["split"] for q in questions)
filters = Counter(q["split"] for q in questions if q.get("filter"))
print(f"questions={len(questions)} splits={dict(splits)} filter_questions={dict(filters)}")
if len(set(ids)) != len(ids):
    errors.append("duplicate question ids")
if splits["dev"] < 15 or splits["test"] < 5:
    errors.append("need at least 15 dev and 5 test questions")
if sum(filters.values()) < 3 or filters["test"] < 1:
    errors.append("need >=3 filter questions with >=1 in test")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("All evidence quotes verified on their gold pages.")
