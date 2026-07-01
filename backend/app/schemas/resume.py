from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    filename: str
    pages: int
    characters: int
    preview: str