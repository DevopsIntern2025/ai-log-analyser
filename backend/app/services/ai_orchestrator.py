from sqlalchemy.orm import Session

from app.models.log_file import LogFile
from app.services.log_parser import parse_log_content
from app.services.prompt_builder import build_analysis_prompt
from app.services.gemini_service import generate_analysis


async def analyze_log(
    log_file: LogFile,
    db: Session,
) -> dict:

    with open(
        log_file.file_path,
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()

    parsed_logs = parse_log_content(content)

    if not parsed_logs:
        return {
            "log_id": log_file.id,
            "filename": log_file.original_filename,
            "status": "no_parseable_logs",
            "analysis": None,
        }

    prompt = build_analysis_prompt(parsed_logs)

    analysis = await generate_analysis(prompt)

    return {
    "log_id": log_file.id,
    "filename": log_file.original_filename,
    "status": "analyzed",
    "analysis": analysis.model_dump(),
    "parsed_log_count": len(parsed_logs),
 }