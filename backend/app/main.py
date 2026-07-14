from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis import router as analysis_router
from app.api.health import router as health_router
from app.api.information import router as information_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging

logger = get_logger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging()
    logger.info("Starting AI Entrepreneur Radar backend (env=%s)", settings.app_env)
    yield
    logger.info("Shutting down AI Entrepreneur Radar backend")


app = FastAPI(
    title="AI Entrepreneur Radar",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(information_router)
app.include_router(analysis_router)
