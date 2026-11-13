"""Day 06 pipeline entry point.

Run from starter/:
  python -m src.run ingest              # chunk A/B, embed new/changed chunks, store in pgvector
  python -m src.run evaluate --split dev
  python -m src.run evaluate --split test   # only after the strategy is chosen on dev
  python -m src.run audit               # sheets for manual coherence / metadata / grounding labels
"""
import argparse
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from .chunking import by_paragraph, fixed_size
from .embeddings import build_embedder
from .evaluation import evaluate_query, summarize
from .ingestion import load_pdf
from .models import Chunk, DocumentPage
from .store import PgVectorStore, content_hash

STARTER = Path(__file__).resolve().parents[1]
REPO = STARTER.parent
RESULTS = STARTER / "results"
# USD per 1M input tokens for text-embedding-3-small (OpenAI pricing page; re-check if model changes).
PRICE_PER_M_TOKENS = {"text-embedding-3-small": 0.02}

STRATEGIES = {
    "A": {"chunking": "fixed_size", "size": 500, "overlap": 50, "index": "A", "use_filter": False},
    "B": {"chunking": "by_paragraph", "max_size": 800, "min_size": 80, "index": "B", "use_filter": False},
    # C reuses B's chunks and vectors; the only difference is the chapter filter.
    "C": {"chunking": "by_paragraph (same index as B)", "index": "B", "use_filter": True},
}
INDEXES = {
    "A": lambda page: fixed_size(page, 500, 50, strategy="A"),
    "B": lambda page: by_paragraph(page, 800, min_size=80, strategy="B"),
}


def load_corpus() -> list[DocumentPage]:
    config = json.loads((STARTER / "corpus.json").read_text(encoding="utf-8"))
    manifest = json.loads((REPO / "data" / "manifest.json").read_text(encoding="utf-8"))
    counted = {p["pdf_page"] for p in manifest["pages"] if p["counted"]}
    pdf = STARTER / config["local_path"]
    if not pdf.exists():
        sys.exit("Corpus PDF missing: run python scripts/download_corpus.py")
    pages = []
    for chapter in config["chapters"]:
        for page in load_pdf(pdf, config["source_id"], config["local_path"],
                             chapter["pdf_first_page"], chapter["pdf_last_page"]):
            if page.page not in counted:
                continue
            page.metadata = {"chapter": chapter["chapter"], "chapter_title": chapter["title"],
                             "book_page": page.metadata.get("book_page")}
            pages.append(page)
    if len(pages) < 30:
        sys.exit(f"Only {len(pages)} content pages; need >= 30")
    return pages


def load_questions(split: str) -> list[dict]:
    lines = (REPO / "benchmark" / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    questions = [json.loads(line) for line in lines if line.strip()]
    return [q for q in questions if split == "all" or q["split"] == split]


def make_store(dimensions: int) -> PgVectorStore:
    load_dotenv(STARTER / ".env")
    url = os.getenv("DATABASE_URL")
    if not url:
        sys.exit("DATABASE_URL missing in starter/.env")
    return PgVectorStore(url, dimensions)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ingest() -> None:
    pages = load_corpus()
    embedder = build_embedder()
    store = make_store(embedder.dimensions)
    store.create_schema()
    stats = {"run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "embedding_provider": embedder.provider, "embedding_model": embedder.model_name,
             "dimensions": embedder.dimensions, "content_pages": len(pages), "indexes": {}}
    for name, chunker in INDEXES.items():
        t0 = time.perf_counter()
        chunks: list[Chunk] = [c for page in pages for c in chunker(page)]
        t_chunk = time.perf_counter() - t0
        existing = store.existing_hashes(name)
        changed = [c for c in chunks
                   if existing.get(c.chunk_id) != content_hash(c.text, embedder.model_name)]
        tokens_before = embedder.total_tokens
        t0 = time.perf_counter()
        vectors = embedder.embed_documents([c.text for c in changed]) if changed else []
        t_embed = time.perf_counter() - t0
        t0 = time.perf_counter()
        result = store.upsert(name, changed, vectors, embedder.model_name,
                              {p.document_id for p in pages}, [c.chunk_id for c in chunks])
        t_store = time.perf_counter() - t0
        tokens = embedder.total_tokens - tokens_before
        lengths = [len(c.text) for c in chunks]
        stats["indexes"][name] = {
            "chunks": len(chunks), "rows_in_db": store.count(name),
            "embedded_this_run": len(changed), "skipped_unchanged": len(chunks) - len(changed),
            "deleted_obsolete": result["deleted_obsolete"],
            "chars_total": sum(lengths), "len_min": min(lengths), "len_median": statistics.median(lengths),
            "len_mean": round(statistics.mean(lengths), 1), "len_max": max(lengths),
            "embedding_tokens_this_run": tokens,
            "cost_usd_this_run": round(tokens / 1e6 * PRICE_PER_M_TOKENS.get(embedder.model_name, 0), 6),
            "seconds": {"chunk": round(t_chunk, 3), "embed": round(t_embed, 2), "store": round(t_store, 2)},
        }
        print(name, json.dumps(stats["indexes"][name]))
    history = RESULTS / "ingest_runs.jsonl"
    with history.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(stats, ensure_ascii=False) + "\n")
    write_json(RESULTS / "ingest_stats.json", stats)


def evaluate(split: str) -> None:
    questions = load_questions(split)
    embedder = build_embedder()
    store = make_store(embedder.dimensions)
    t0 = time.perf_counter()
    query_vectors = embedder.embed_documents([q["question"] for q in questions])
    t_query_embed = time.perf_counter() - t0
    traces = []
    for strategy, cfg in STRATEGIES.items():
        t0 = time.perf_counter()
        for q, qv in zip(questions, query_vectors):
            applied = q.get("filter") if cfg["use_filter"] else None
            hits = store.search(cfg["index"], qv, top_k=3, filters=applied)
            traces.append({
                "strategy": strategy, "index": cfg["index"], "id": q["id"], "split": q["split"],
                "type": q["type"], "question": q["question"], "requested_filter": q.get("filter"),
                "applied_filter": applied, "gold_page": q["gold_page"],
                "alt_gold_pages": [a["gold_page"] for a in q.get("alternatives", [])],
                "evidence_quote": q["evidence_quote"], "expected_answer": q["expected_answer"],
                "top3": hits, "evaluation": evaluate_query(q, hits),
            })
        print(f"{strategy}: {len(questions)} queries in {time.perf_counter() - t0:.2f}s")
    with (RESULTS / f"traces_{split}.jsonl").open("w", encoding="utf-8") as handle:
        for trace in traces:
            handle.write(json.dumps(trace, ensure_ascii=False) + "\n")
    summary = summarize(traces)
    meta = {"run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "split": split,
            "embedding_model": embedder.model_name, "query_embedding_tokens": embedder.total_tokens,
            "query_embedding_seconds": round(t_query_embed, 2), "strategies": STRATEGIES}
    write_json(RESULTS / f"metrics_{split}.json", {"meta": meta, "summary": summary})
    print(f"{'strategy':8} {'split':5} {'Hit@1':>6} {'EvHit@3':>8} {'PageHit@3':>9} {'filter':>7}  misses")
    for b in summary.values():
        print(f"{b['strategy']:8} {b['split']:5} {b['hit@1']:>6} {b['evidence_hit@3']:>8} "
              f"{b['page_hit@3']:>9} {b['filter_compliance']:>7}  {','.join(b['misses'])}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ingest")
    ev = sub.add_parser("evaluate")
    ev.add_argument("--split", choices=["dev", "test"], required=True)
    sub.add_parser("audit")
    args = parser.parse_args()
    RESULTS.mkdir(exist_ok=True)
    if args.cmd == "ingest":
        ingest()
    elif args.cmd == "evaluate":
        evaluate(args.split)
    else:
        from .audit import build_audit_sheets
        build_audit_sheets(load_corpus(), INDEXES, RESULTS)


if __name__ == "__main__":
    main()
