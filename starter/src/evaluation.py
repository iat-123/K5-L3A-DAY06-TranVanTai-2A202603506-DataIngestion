"""Automatic retrieval metrics and per-query traces.

Evidence hit: the retrieved chunk is on a gold page (primary or documented
alternative) AND contains the whole evidence quote (whitespace-insensitive).
Coherence and grounding are NOT inferred here; they are labelled manually.
"""
import re
from typing import Any


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _golds(question: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"gold_page": question["gold_page"], "evidence_quote": question["evidence_quote"]}] + \
        question.get("alternatives", [])


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    golds = _golds(question)
    gold_pages = {g["gold_page"] for g in golds}
    flags = []
    for hit in hits:
        text = squash(hit["text"])
        evidence_hit = any(hit["page"] == g["gold_page"] and squash(g["evidence_quote"]) in text
                           for g in golds)
        flags.append({"chunk_id": hit["chunk_id"], "page_hit": hit["page"] in gold_pages,
                      "evidence_hit": evidence_hit})
    filt = question.get("filter")
    filter_ok = None
    if filt:
        filter_ok = all(all(hit.get(k) == v for k, v in filt.items()) for hit in hits)
    # Gold page retrieved but no retrieved chunk holds the full quote. This does NOT prove the
    # evidence is split: another chunk of that page may hold it but rank below top-3. Check the
    # full chunk set of the gold page before calling it a split (done in the report analysis).
    split_suspect = any(f["page_hit"] for f in flags) and not any(f["evidence_hit"] for f in flags)
    return {
        "hit@1": bool(flags and flags[0]["evidence_hit"]),
        "hit@3": any(f["evidence_hit"] for f in flags[:3]),
        "page_hit@3": any(f["page_hit"] for f in flags[:3]),
        "evidence_split_or_partial": split_suspect,
        "filter_compliant": filter_ok,
        "per_hit": flags,
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 / Evidence Hit@3 by strategy and split, as n/N counts."""
    out: dict[str, Any] = {}
    for trace in traces:
        key = f"{trace['strategy']}|{trace['split']}"
        bucket = out.setdefault(key, {"strategy": trace["strategy"], "split": trace["split"], "N": 0,
                                      "hit1": 0, "hit3": 0, "page_hit3": 0,
                                      "filter_N": 0, "filter_ok": 0, "misses": []})
        ev = trace["evaluation"]
        bucket["N"] += 1
        bucket["hit1"] += ev["hit@1"]
        bucket["hit3"] += ev["hit@3"]
        bucket["page_hit3"] += ev["page_hit@3"]
        # Measured for every strategy on filter questions: for A/B it shows whether results
        # happen to stay in the requested chapter without filtering.
        if ev["filter_compliant"] is not None:
            bucket["filter_N"] += 1
            bucket["filter_ok"] += ev["filter_compliant"]
        if not ev["hit@3"]:
            bucket["misses"].append(trace["id"])
    for bucket in out.values():
        bucket["hit@1"] = f"{bucket['hit1']}/{bucket['N']}"
        bucket["evidence_hit@3"] = f"{bucket['hit3']}/{bucket['N']}"
        bucket["page_hit@3"] = f"{bucket['page_hit3']}/{bucket['N']}"
        bucket["filter_compliance"] = (f"{bucket['filter_ok']}/{bucket['filter_N']}"
                                       if bucket["filter_N"] else "N/A")
    return out
