"""Fixed-size and structure-aware chunking.

Every chunk is a contiguous span of ONE page's normalized text (chunk.text ==
page.text[start:end]), so page metadata stays exact and character offsets can
be used to locate chunks for manual audits.
"""
import re

from .models import Chunk, DocumentPage

# Lines that start a new logical block in OpenStax pages.
HEADING = re.compile(
    r"^(\d+\.\d+ [A-Z].*"                       # section heading: "5.2 For loop"
    r"|Learning objectives"
    r"|CHECKPOINT|CONCEPTS IN PRACTICE|TRY IT|EXPLORING FURTHER"
    r"|EXAMPLE \d+\.\d+"
    r"|[A-Z0-9][A-Z0-9 :=/,'\-]{3,})$"          # all-caps callout title, e.g. "INFINITE LOOP"
)
SENTENCE_END = re.compile(r"[.!?:]$")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
# Short title-case subsection title such as "Continue", "Local scope", "Range() function in for loop".
SUBTITLE = re.compile(r"^[A-Z][A-Za-z()\- ]{0,45}$")
PROSE_START = re.compile(r"^(A|An|The|In|When|If|Sometimes|Functions|Python|So far|What)\b")


def _is_heading(line: str, next_line: str) -> bool:
    if HEADING.match(line):
        return True
    # A subtitle is only accepted when the next line starts an explanatory sentence.
    return bool(SUBTITLE.match(line)) and len(line.split()) <= 6 and bool(PROSE_START.match(next_line))


def _make_chunk(page: DocumentPage, strategy: str, index: int, start: int, end: int) -> Chunk:
    metadata = dict(page.metadata)
    metadata.update(start=start, end=end, strategy=strategy)
    return Chunk(
        chunk_id=f"{page.document_id}:p{page.page:03d}:{strategy}:{index:02d}",
        document_id=page.document_id, source=page.source, page=page.page,
        text=page.text[start:end], metadata=metadata,
    )


def fixed_size(page: DocumentPage, size: int, overlap: int, strategy: str = "A") -> list[Chunk]:
    """Character windows of `size` with `overlap`, ignoring sentence/heading boundaries."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    text, chunks, start = page.text, [], 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(_make_chunk(page, strategy, len(chunks), start, end))
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _paragraph_spans(text: str) -> list[tuple[int, int, bool]]:
    """Return (start, end, is_heading) spans.

    pypdf gives hard-wrapped lines without blank lines between paragraphs, so a
    paragraph ends at a line ending with sentence punctuation, and a heading /
    callout line is always its own block.
    """
    spans: list[tuple[int, int, bool]] = []
    para_start = None
    offset = 0
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line_start, line_end = offset, offset + len(line)
        offset = line_end + 1
        if not line.strip():
            if para_start is not None:
                spans.append((para_start, line_start - 1, False))
                para_start = None
            continue
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if _is_heading(line.strip(), next_line):
            if para_start is not None:
                spans.append((para_start, line_start - 1, False))
                para_start = None
            spans.append((line_start, line_end, True))
            continue
        if para_start is None:
            para_start = line_start
        if SENTENCE_END.search(line.strip()):
            spans.append((para_start, line_end, False))
            para_start = None
    if para_start is not None:
        spans.append((para_start, len(text), False))
    return spans


def _split_long(text: str, start: int, end: int, max_size: int) -> list[tuple[int, int]]:
    """Split an oversized paragraph at sentence boundaries, hard-cutting only as a last resort."""
    pieces, piece_start = [], start
    cuts = [start + m.end() for m in SENTENCE_SPLIT.finditer(text[start:end])] + [end]
    last_cut = start
    for cut in cuts:
        if cut - piece_start > max_size and last_cut > piece_start:
            pieces.append((piece_start, last_cut))
            piece_start = last_cut
        last_cut = cut
    pieces.append((piece_start, end))
    result = []
    for s, e in pieces:  # hard cut for a single sentence longer than max_size
        while e - s > max_size:
            result.append((s, s + max_size))
            s += max_size
        result.append((s, e))
    return result


def by_paragraph(page: DocumentPage, max_size: int, min_size: int = 80,
                 strategy: str = "B") -> list[Chunk]:
    """Group paragraphs up to `max_size` chars; headings start a new chunk.

    A heading starts a new chunk only when the current chunk already has at least
    `min_size` characters, so a short heading stays attached to its content.
    """
    text = page.text
    spans: list[tuple[int, int, bool]] = []
    for start, end, is_heading in _paragraph_spans(text):
        if end - start > max_size:
            spans.extend((s, e, False) for s, e in _split_long(text, start, end, max_size))
        else:
            spans.append((start, end, is_heading))

    groups: list[tuple[int, int]] = []
    cur_start = cur_end = None
    for start, end, is_heading in spans:
        if cur_start is None:
            cur_start, cur_end = start, end
            continue
        too_big = end - cur_start > max_size
        heading_break = is_heading and (cur_end - cur_start) >= min_size
        if too_big or heading_break:
            groups.append((cur_start, cur_end))
            cur_start, cur_end = start, end
        else:
            cur_end = end
    if cur_start is not None:
        groups.append((cur_start, cur_end))
    # Fold fragments shorter than `tiny` into the neighbouring chunk (page-end leftovers).
    tiny = 100
    merged: list[tuple[int, int]] = []
    for start, end in groups:
        if merged and end - start < tiny:
            merged[-1] = (merged[-1][0], end)
        elif merged and merged[-1][1] - merged[-1][0] < tiny:
            merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))
    return [_make_chunk(page, strategy, i, s, e) for i, (s, e) in enumerate(merged)]
