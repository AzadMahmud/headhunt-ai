from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.services.resume_service import analyze_and_store, save_resume_file
from app.services.pdf_parser import extract_text, generate_metadata
from app.repositories.resume_repository import ResumeRepository
from app.api.deps import get_resume_repository
from app.schemas.resume import (
    ResumeUploadResponse,
    ResumeHistoryItem,
    ResumeDetailResponse,
)
from app.schemas.analysis import ResumeAnalysisResponse

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    saved_path, _ = save_resume_file(file)
    text, pages = extract_text(saved_path)
    metadata = generate_metadata(text, pages)

    return ResumeUploadResponse(
        filename=saved_path.name,
        pages=metadata["pages"],
        characters=metadata["characters"],
        preview=metadata["preview"],
    )


@router.post("/analyze", response_model=ResumeDetailResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    repo: ResumeRepository = Depends(get_resume_repository),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    resume = analyze_and_store(file, repo)
    return resume


@router.get("/", response_model=list[ResumeHistoryItem])
async def list_resumes(
    skip: int = 0,
    limit: int = 20,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    return repo.list_all(skip=skip, limit=limit)


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
async def get_resume(
    resume_id: int,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    resume = repo.get_by_id(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    return resume


@router.delete("/{resume_id}", status_code=204)
async def delete_resume(
    resume_id: int,
    repo: ResumeRepository = Depends(get_resume_repository),
):
    resume = repo.get_by_id(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")
    repo.delete(resume)