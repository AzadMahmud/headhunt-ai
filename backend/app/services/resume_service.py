from pathlib import Path
import uuid
from fastapi import UploadFile

from app.services.pdf_parser import extract_text
from app.services.llm_service import analyze_resume as llm_analyze
from app.schemas.analysis import ResumeAnalysisResponse

UPLOAD_DIR = Path("uploads")


def save_resume(file: UploadFile) -> Path:
    """
    Save uploaded resume to disk.
    """

    UPLOAD_DIR.mkdir(exist_ok=True)

    suffix = Path(file.filename).suffix

    unique_filename = f"{uuid.uuid4()}{suffix}"

    destination = UPLOAD_DIR / unique_filename

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    return destination


def analyze_resume(file: UploadFile) -> ResumeAnalysisResponse:
    saved_path = save_resume(file)
    text, _ = extract_text(saved_path)
    return llm_analyze(text)
