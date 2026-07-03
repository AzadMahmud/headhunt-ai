from sqlmodel import Session, select

from app.models.resume import Resume


class ResumeRepository:
    """Only this class is allowed to know SQL. Everything else calls it."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, resume: Resume) -> Resume:
        self.session.add(resume)
        self.session.commit()
        self.session.refresh(resume)
        return resume

    def get_by_id(self, resume_id: int) -> Resume | None:
        return self.session.get(Resume, resume_id)

    def list_all(self, skip: int = 0, limit: int = 20) -> list[Resume]:
        statement = (
            select(Resume)
            .order_by(Resume.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.exec(statement).all())

    def delete(self, resume: Resume) -> None:
        self.session.delete(resume)
        self.session.commit()