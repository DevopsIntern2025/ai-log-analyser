from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.api.v1.auth import get_current_user
from app.models.user import User
from app.services.log_service import save_log_file
from app.db.database import get_db
from app.models.log_file import LogFile
from app.services.log_parser import parse_log_content


router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.post("/upload")
async def upload_log(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = await save_log_file(file)

    log_file = LogFile(
        user_id=current_user.id,
        original_filename=result["original_filename"],
        stored_filename=result["stored_filename"],
        file_path=result["file_path"],
        file_size=result["file_size"],
        status="uploaded",
    )

    db.add(log_file)
    db.commit()
    db.refresh(log_file)

    return {
        "message": "Log uploaded successfully",
        "log_id": log_file.id,
        "user_id": current_user.id,
        "original_filename": log_file.original_filename,
        "stored_filename": log_file.stored_filename,
        "file_size": log_file.file_size,
        "status": log_file.status,
    }

@router.get("")
def get_user_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(LogFile)
        .filter(
            LogFile.user_id == current_user.id
        )
        .order_by(
            LogFile.created_at.desc()
        )
        .all()
    )

    return {
        "user_id": current_user.id,
        "count": len(logs),
        "logs": [
            {
                "id": log.id,
                "original_filename": log.original_filename,
                "stored_filename": log.stored_filename,
                "file_size": log.file_size,
                "status": log.status,
                "created_at": log.created_at,
            }
            for log in logs
        ],
    }

@router.get("/{log_id}/parsed")
def parse_uploaded_log(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log file not found",
        )

    try:
        with open(
            log_file.file_path,
            "r",
            encoding="utf-8",
        ) as file:
            content = file.read()

    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Physical log file not found",
        )

    parsed_logs = parse_log_content(content)

    return {
        "log_id": log_file.id,
        "filename": log_file.original_filename,
        "count": len(parsed_logs),
        "logs": parsed_logs,
    }