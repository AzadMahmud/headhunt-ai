from datetime import datetime

from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    filename: str
    pages: int
    characters: int
    preview: str

class ResumeHistoryItem(BaseModel):
    id: int
    original_filename: str
    pages: int
    created_at: datetime


class ResumeDetailResponse(BaseModel):
    id: int
    original_filename: str
    pages: int
    characters: int
    preview: str
    strengths: list[str] | None
    weaknesses: list[str] | None
    missing_skills: list[str] | None
    recommendations: list[str] | None
    created_at: datetime