from fastapi import FastAPI

from app.core.config import settings
from app.db.database import Base, engine
from app.db import base
from app.api.v1.auth import router as auth_router
from app.api.v1.logs import router as logs_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered application log analyzer using Google Gemini",
    version=settings.APP_VERSION,
)

app.include_router(auth_router)
app.include_router(logs_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Log Analyzer 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "UP"
    }

@app.get("/config")
def show_config():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": settings.DATABASE_URL,
    }