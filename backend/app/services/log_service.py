from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


async def save_log_file(
    file: UploadFile,
) -> dict:

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    original_filename = Path(file.filename).name

    extension = Path(
        original_filename
    ).suffix.lower()

    if extension not in settings.ALLOWED_LOG_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid file type. "
                "Only .log and .txt files are allowed."
            ),
        )

    content = await file.read()

    max_size = (
        settings.MAX_UPLOAD_SIZE_MB
        * 1024
        * 1024
    )

    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"File too large. "
                f"Maximum size is "
                f"{settings.MAX_UPLOAD_SIZE_MB} MB."
            ),
        )

    safe_filename = (
        f"{uuid4().hex}{extension}"
    )

    file_path = UPLOAD_DIR / safe_filename

    file_path.write_bytes(content)

    return {
        "original_filename": original_filename,
        "stored_filename": safe_filename,
        "file_path": str(file_path),
        "file_size": len(content),
    }