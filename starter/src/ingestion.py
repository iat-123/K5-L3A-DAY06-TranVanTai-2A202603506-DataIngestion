"""Read and normalize source data.

OpenStax PDFs carry a running footer on every page:
  odd pages : "<chapter>.<n> • <section title>     <book page>"
  even pages: "<book page>     <chapter> • <chapter title>"
  all pages : "Access for free at openstax.org"
These lines are removed from the text and parsed into metadata, so chapter
information comes from the source itself rather than being guessed.
"""
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

from .models import DocumentPage

ATTRIBUTION = "Access for free at openstax.org"
# "4.1 • Boolean values     87"
ODD_FOOTER = re.compile(r"^(\d+)\.(\d+)\s*•\s*(.+?)\s{2,}(\d+)$")
# "88     4 • Decisions"
EVEN_FOOTER = re.compile(r"^(\d+)\s{2,}(\d+)\s*•\s*(.+)$")


def normalize_text(text: str) -> str:
    """Normalize Unicode (NFC) and whitespace while keeping line structure.

    - NFC so composed/decomposed characters compare equal.
    - Non-breaking / odd spaces become plain spaces; runs of spaces collapse.
    - Trailing spaces stripped per line; 3+ blank lines collapse to one blank line.
    Line breaks are kept because headings and code lines depend on them.
    """
    text = unicodedata.normalize("NFC", text)
    text = text.replace(" ", " ").replace(" ", " ").replace(" ", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _split_footer(raw: str) -> tuple[str, dict]:
    """Remove running footer lines; return (body_text, footer_metadata)."""
    meta: dict = {}
    kept: list[str] = []
    for line in raw.split("\n"):
        stripped = line.strip()
        if stripped == ATTRIBUTION:
            continue
        # Footer lines keep their multi-space gap before normalization.
        m = ODD_FOOTER.match(stripped)
        if m:
            meta.update(chapter=int(m.group(1)), footer_section=f"{m.group(1)}.{m.group(2)}",
                        footer_section_title=m.group(3).strip(), book_page=int(m.group(4)))
            continue
        m = EVEN_FOOTER.match(stripped)
        if m:
            meta.update(book_page=int(m.group(1)), chapter=int(m.group(2)),
                        chapter_title=m.group(3).strip())
            continue
        kept.append(line)
    return "\n".join(kept), meta


def load_pdf(path: Path, document_id: str, source: str,
             first_page: int = 1, last_page: int | None = None) -> list[DocumentPage]:
    """Extract each physical page (1-based, inclusive range) with its page number.

    Pages with no extractable text are still returned (empty text) so callers can
    log them; OCR is not attempted here.
    """
    reader = PdfReader(str(path))
    last_page = last_page or len(reader.pages)
    pages: list[DocumentPage] = []
    for number in range(first_page, last_page + 1):
        raw = reader.pages[number - 1].extract_text() or ""
        raw = unicodedata.normalize("NFC", raw).replace(" ", " ")
        body, footer = _split_footer(raw)
        pages.append(DocumentPage(document_id=document_id, source=source, page=number,
                                  text=normalize_text(body), metadata=footer))
    return pages
