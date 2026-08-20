from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.database import Base

from sqlalchemy.orm import relationship


class LogFile(Base):
    __tablename__ = "log_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    original_filename = Column(
        String(255),
        nullable=False,
    )

    stored_filename = Column(
        String(255),
        nullable=False,
        unique=True,
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    file_size = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        String(50),
        nullable=False,
        default="uploaded",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    analyses = relationship(
    "AIAnalysis",
    back_populates="log_file",
    cascade="all, delete-orphan",
    )