from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)

    log_file_id = Column(
        Integer,
        ForeignKey("log_files.id"),
        nullable=False,
        index=True,
    )

    severity = Column(
        String(20),
        nullable=False,
    )

    summary = Column(
        Text,
        nullable=False,
    )

    root_cause = Column(
        Text,
        nullable=False,
    )

    evidence = Column(
        JSON,
        nullable=False,
    )

    recommendations = Column(
        JSON,
        nullable=False,
    )

    risk = Column(
        Text,
        nullable=False,
    )

    confidence = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    log_file = relationship(
    "LogFile",
    back_populates="analyses",
    )