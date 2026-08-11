from fastapi import FastAPI
from app.core.config import settings
from app.db.database import Base, engine
from app.db import base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered application log analyzer using Google Gemini",
    version=settings.APP_VERSION,
)

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