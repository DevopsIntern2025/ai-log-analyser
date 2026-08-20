from sqlalchemy.orm import Session

from app.models.log_file import LogFile
from app.models.ai_analysis import AIAnalysis
from app.services.log_parser import parse_log_content
from app.services.prompt_builder import build_analysis_prompt
from app.services.gemini_service import generate_analysis
from app.services.error_analyzer import analyze_errors


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

    error_analysis = analyze_errors(parsed_logs)

    if not parsed_logs:
        return {
            "log_id": log_file.id,
            "filename": log_file.original_filename,
            "status": "no_parseable_logs",
            "analysis": None,
        }

    prompt = build_analysis_prompt(parsed_logs,error_analysis,)

    analysis = await generate_analysis(prompt)

    ai_analysis = AIAnalysis(
    log_file_id=log_file.id,
    severity=analysis.severity,
    summary=analysis.summary,
    root_cause=analysis.root_cause,
    evidence=analysis.evidence,
    recommendations=analysis.recommendations,
    risk=analysis.risk,
    confidence=analysis.confidence,
    )

    db.add(ai_analysis)
    db.commit()
    db.refresh(ai_analysis)

    return {
    "log_id": log_file.id,
    "filename": log_file.original_filename,
    "status": "analyzed",
    "analysis_id": ai_analysis.id,
    "analysis": analysis.model_dump(),
    "parsed_log_count": len(parsed_logs),
 }