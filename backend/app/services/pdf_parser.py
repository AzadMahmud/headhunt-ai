from pathlib import Path

from pypdf import PdfReader


def extract_text(pdf_path: Path) -> tuple[str, int]:
    """
    Extract text from a PDF.

    Returns:
        tuple(text, page_count)
    """

    reader = PdfReader(pdf_path)

    pages = len(reader.pages)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text, pages


def generate_metadata(text: str, pages: int) -> dict:
    return {"pages": pages, "characters": len(text), "preview": text[:300]}
