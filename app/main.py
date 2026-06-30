from fastapi import FastAPI
from app.api.resume import router as resume_router

app = FastAPI(
    title="HeadHunt AI",
    version="0.1.0"
)

app.include_router(resume_router)