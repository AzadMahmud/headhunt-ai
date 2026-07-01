from pydantic import BaseModel


class ResumeAnalysisResponse(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    missing_skills: list[str]
    recommendations: list[str]