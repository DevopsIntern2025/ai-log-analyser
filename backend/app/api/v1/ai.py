from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth import get_current_user
from app.db.database import get_db
from app.models.log_file import LogFile
from app.models.ai_analysis import AIAnalysis
from app.models.user import User
from app.services.ai_orchestrator import analyze_log


router = APIRouter(
    prefix="/ai",
    tags=["AI Analysis"],
)


@router.post("/analyze/{log_id}")
async def analyze_uploaded_log(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    log_file = (
        db.query(LogFile)
        .filter(
            LogFile.id == log_id,
            LogFile.user_id == current_user.id,
        )
        .first()
    )

    if not log_file:
        raise HTTPException(
            status_code=404,
            detail="Log file not found",
        )

    return await analyze_log(
        log_file=log_file,
        db=db,
    )

@router.get("/analysis/{log_id}")
async def get_analysis(
    log_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    log_file = (
        db.query(LogFile)
        .filter(
            LogFile.id == log_id,
            LogFile.user_id == current_user.id,
        )
        .first()
    )

    if not log_file:
        raise HTTPException(
            status_code=404,
            detail="Log file not found",
        )

    analysis = (
        db.query(AIAnalysis)
        .filter(
            AIAnalysis.log_file_id == log_file.id,
        )
        .order_by(AIAnalysis.created_at.desc())
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="AI analysis not found for this log",
        )

    return {
        "analysis_id": analysis.id,
        "log_id": analysis.log_file_id,
        "severity": analysis.severity,
        "summary": analysis.summary,
        "root_cause": analysis.root_cause,
        "evidence": analysis.evidence,
        "recommendations": analysis.recommendations,
        "risk": analysis.risk,
        "confidence": analysis.confidence,
        "created_at": analysis.created_at,
    }
