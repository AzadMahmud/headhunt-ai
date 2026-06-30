from fastapi import APIRouter, UploadFile, File

from app.services.resume_service import save_resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    saved_path = save_resume(file)

    return {
        "filename": file.filename,
        "saved_to": str(saved_path)
    }