from pydantic import BaseModel, Field


class AIAnalysis(BaseModel):
    severity: str = Field(
        description="Overall severity of the incident"
    )

    summary: str = Field(
        description="Short summary of the problem"
    )

    root_cause: str = Field(
        description="Likely root cause based on the logs"
    )

    evidence: list[str] = Field(
        description="Important log evidence supporting the analysis"
    )

    recommendations: list[str] = Field(
        description="Recommended remediation steps"
    )

    risk: str = Field(
        description="Potential impact if the issue is not resolved"
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the analysis from 0 to 1"
    )