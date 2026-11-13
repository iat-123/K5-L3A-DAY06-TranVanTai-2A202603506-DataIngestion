"""Build ../data/manifest.json and an ingestion log from corpus.json.

Run from starter/:  python scripts/build_manifest.py

Page counting rule: a physical page in the selected chapter range counts as a
content page when its normalized body text (running footer removed) has at
least `min_content_chars` characters. Shorter pages are listed as excluded
with a reason. Chapter numbers come from the table of contents ranges and are
cross-checked against each page's running footer.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.ingestion import load_pdf  # noqa: E402

config = json.loads((ROOT / "corpus.json").read_text(encoding="utf-8"))
pdf_path = ROOT / config["local_path"]
if not pdf_path.exists():
    sys.exit("Corpus PDF missing: run python scripts/download_corpus.py first.")

min_chars = config["min_content_chars"]
pages_out, log = [], []
for chapter in config["chapters"]:
    pages = load_pdf(pdf_path, config["source_id"], config["local_path"],
                     chapter["pdf_first_page"], chapter["pdf_last_page"])
    for page in pages:
        footer_chapter = page.metadata.get("chapter")
        if footer_chapter is not None and footer_chapter != chapter["chapter"]:
            log.append(f"p{page.page}: footer chapter {footer_chapter} != TOC chapter {chapter['chapter']}")
        chars = len(page.text)
        counted = chars >= min_chars
        reason = None
        if chars == 0:
            reason = "no extractable text"
        elif not counted:
            reason = f"only {chars} chars after footer removal (end-of-chapter remainder / link-only page)"
        if reason:
            log.append(f"p{page.page}: excluded - {reason}")
        pages_out.append({
            "page_id": f"{config['source_id']}:p{page.page:03d}",
            "pdf_page": page.page,
            "book_page": page.metadata.get("book_page"),
            "chapter": chapter["chapter"],
            "chapter_title": chapter["title"],
            "chars": chars,
            "counted": counted,
            "exclusion_reason": reason,
        })

counted_pages = [p for p in pages_out if p["counted"]]
manifest = {
    "sources": [{
        "source_id": config["source_id"],
        "title": config["title"],
        "authors": config["authors"],
        "publisher": config["publisher"],
        "source_path_or_url": config["source_url"],
        "local_path": f"starter/{config['local_path']}",
        "book_page_url": config["book_page_url"],
        "license_or_permission": config["license"],
        "accessed_at": config["accessed_at"],
        "snapshot_sha256": config["sha256"],
        "physical_pages_total": config["physical_pages_total"],
        "selected_range": [{k: c[k] for k in ("chapter", "title", "pdf_first_page", "pdf_last_page")}
                           for c in config["chapters"]],
    }],
    "page_counting_rule": (
        f"Physical PDF pages inside the selected chapters; a page counts when its normalized text "
        f"(NFC, whitespace collapsed, running footer and 'Access for free at openstax.org' removed) "
        f"has >= {min_chars} characters. Cover, TOC, preface and other chapters are outside the range."),
    "summary": {
        "physical_pages_in_range": len(pages_out),
        "content_pages_counted": len(counted_pages),
        "excluded_pages": len(pages_out) - len(counted_pages),
        "content_chars_counted": sum(p["chars"] for p in counted_pages),
    },
    "pages": pages_out,
}

out = ROOT.parent / "data" / "manifest.json"
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
log_path = ROOT / "results" / "ingestion_log.txt"
log_path.write_text("\n".join(log) + "\n", encoding="utf-8")
print(json.dumps(manifest["summary"], indent=2))
print(f"Wrote {out} and {log_path} ({len(log)} log lines)")
