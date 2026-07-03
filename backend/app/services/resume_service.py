from pathlib import Path
import uuid
from fastapi import UploadFile

from app.services.pdf_parser import extract_text, generate_metadata
from app.services.llm_service import analyze_resume as llm_analyze
from app.repositories.resume_repository import ResumeRepository
from app.models.resume import Resume

UPLOAD_DIR = Path("uploads")


def save_resume_file(file: UploadFile) -> tuple[Path, str]:
    """Save uploaded resume to disk. Returns (saved_path, original_filename)."""
    UPLOAD_DIR.mkdir(exist_ok=True)

    suffix = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{suffix}"
    destination = UPLOAD_DIR / unique_filename

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    return destination, file.filename


def analyze_and_store(file: UploadFile, repo: ResumeRepository) -> Resume:
    """
    Full pipeline: save file -> extract text -> call LLM -> persist -> return row.
    """
    saved_path, original_filename = save_resume_file(file)
    text, pages = extract_text(saved_path)
    metadata = generate_metadata(text, pages)

    analysis = llm_analyze(text)

    resume = Resume(
        filename=saved_path.name,
        original_filename=original_filename,
        pages=metadata["pages"],
        characters=metadata["characters"],
        preview=metadata["preview"],
        full_text=text,
        strengths=analysis.strengths,
        weaknesses=analysis.weaknesses,
        missing_skills=analysis.missing_skills,
        recommendations=analysis.recommendations,
    )

    return repo.create(resume)