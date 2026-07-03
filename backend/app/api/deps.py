from fastapi import Depends
from sqlmodel import Session

from app.core.database import get_session
from app.repositories.resume_repository import ResumeRepository


def get_resume_repository(
    session: Session = Depends(get_session),
) -> ResumeRepository:
    return ResumeRepository(session)