from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


class Resume(SQLModel, table=True):
    __tablename__ = "resumes"

    id: Optional[int] = Field(default=None, primary_key=True)

    # From upload
    filename: str                 # the uuid-based name saved on disk
    original_filename: str        # what the user actually uploaded
    pages: int
    characters: int
    preview: str
    full_text: str

    # From LLM analysis (nullable — a resume can exist before it's analyzed)
    strengths: Optional[list[str]] = Field(default=None, sa_column=Column(JSON))
    weaknesses: Optional[list[str]] = Field(default=None, sa_column=Column(JSON))
    missing_skills: Optional[list[str]] = Field(default=None, sa_column=Column(JSON))
    recommendations: Optional[list[str]] = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )