from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_service import save_resume, analyze_resume
from app.services.pdf_parser import extract_text, generate_metadata
from app.schemas.resume import ResumeUploadResponse
from app.schemas.analysis import ResumeAnalysisResponse

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    saved_path = save_resume(file)
    text, pages = extract_text(saved_path)
    metadata = generate_metadata(text, pages)

    return ResumeUploadResponse(
        filename=saved_path.name,
        pages=metadata["pages"],
        characters=metadata["characters"],
        preview=metadata["preview"],
    )


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def upload_and_analyze(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    return analyze_resume(file)
