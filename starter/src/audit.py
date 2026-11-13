"""Build manual audit sheets (labels are filled in by a human, not computed here).

- coherence_audit.md : the chunk containing each of the 10 pre-registered source
  positions (middle character of PDF pages 95,103,...,169), per index A and B
  (C uses B's chunks, so its coherence equals B's).
- test_audit.md      : the 6 test questions x strategy x top-3 with metadata to
  check against the source, and blank grounding labels.
"""
import json
from pathlib import Path

COHERENCE_PAGES = [95, 103, 111, 119, 128, 136, 144, 153, 161, 169]


def _block(text: str) -> str:
    return "\n".join("    " + line for line in text.split("\n"))


def build_audit_sheets(pages, indexes, results: Path) -> None:
    by_page = {p.page: p for p in pages}
    out = ["# Coherence audit — 10 vị trí chốt trước (giữa trang)", "",
           "Thang: 0 = cắt giữa ý / thiếu chủ thể; 1 = hiểu một phần, thiếu ngữ cảnh; 2 = tự hiểu, giữ trọn ý.",
           "C dùng chung chunk với B nên điểm coherence của C = B.", ""]
    for number in COHERENCE_PAGES:
        page = by_page[number]
        pos = len(page.text) // 2
        out.append(f"## Trang PDF {number} — vị trí ký tự {pos}")
        out.append(f"Ngữ cảnh nguồn quanh vị trí: `…{page.text[max(0, pos - 60):pos + 60].replace(chr(10), ' / ')}…`")
        out.append("")
        for name, chunker in indexes.items():
            chunk = next(c for c in chunker(page) if c.metadata["start"] <= pos < c.metadata["end"])
            out += [f"### {name}: `{chunk.chunk_id}` [{chunk.metadata['start']}:{chunk.metadata['end']}]",
                    _block(chunk.text), "", f"- Điểm {name}: ", f"- Lý do {name}: ", ""]
    (results / "coherence_audit.md").write_text("\n".join(out), encoding="utf-8")

    traces = [json.loads(line) for line in
              (results / "traces_test.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    out = ["# Test audit — metadata và grounding (6 câu test × A/B/C × top-3)", "",
           "Metadata: so `source`, `page`, `chapter` của từng kết quả với PDF. Cột auto-check chỉ là trợ giúp:",
           "text chunk có nằm đúng ở trang ghi trong metadata không, và chapter có khớp mục lục không.",
           "Grounding (cho cả top-3 của một câu): 0 = không có bằng chứng; 1 = có nhưng thiếu điều kiện/ngữ cảnh;",
           "2 = đủ để trả lời và truy nguồn.", ""]
    chapter_of = {p.page: p.metadata["chapter"] for p in pages}
    for trace in traces:
        out += [f"## {trace['strategy']} · {trace['id']} ({trace['type']}) — {trace['question']}",
                f"- Gold: trang {trace['gold_page']}"
                + (f" (hoặc {trace['alt_gold_pages']})" if trace["alt_gold_pages"] else "")
                + f"; filter yêu cầu: {trace['requested_filter']}; filter áp dụng: {trace['applied_filter']}",
                f"- Evidence: \"{trace['evidence_quote']}\"",
                f"- Tự động: Hit@1={trace['evaluation']['hit@1']}, Evidence Hit@3={trace['evaluation']['hit@3']}", ""]
        for hit in trace["top3"]:
            page = by_page.get(hit["page"])
            on_page = bool(page) and hit["text"] in page.text
            chapter_ok = chapter_of.get(hit["page"]) == hit["chapter"]
            out += [f"### #{hit['rank']} `{hit['chunk_id']}` score={hit['score']}",
                    f"- source={hit['source']} · page={hit['page']} · chapter={hit['chapter']} · "
                    f"book_page={hit['metadata'].get('book_page')}",
                    f"- auto-check: text_on_page={on_page}, chapter_matches_toc={chapter_ok}",
                    _block(hit["text"]), "",
                    "- Metadata đủ và đúng (có/không, lỗi): ", ""]
        out += [f"**Grounding {trace['strategy']}·{trace['id']} (0/1/2):** ", "**Lý do:** ", "", "---", ""]
    (results / "test_audit.md").write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {results / 'coherence_audit.md'} and {results / 'test_audit.md'}")
