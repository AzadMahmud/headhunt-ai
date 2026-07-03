from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.resume import router as resume_router
from app.api.health import router as health_router
from app.core.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev convenience only. Real schema changes go through Alembic (Step 12).
    create_db_and_tables()
    yield


app = FastAPI(
    title="HeadHunt AI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(resume_router)