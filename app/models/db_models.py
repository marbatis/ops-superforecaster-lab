from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ForecastQuestionRecord(Base):
    __tablename__ = "forecast_questions"

    question_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    target_type: Mapped[str] = mapped_column(String(64))
    question_text: Mapped[str] = mapped_column(String(500))
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class ForecastSubmissionRecord(Base):
    __tablename__ = "forecast_submissions"
    __table_args__ = (UniqueConstraint("question_id", "participant", "source_type", name="uq_submission"),)

    submission_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[str] = mapped_column(ForeignKey("forecast_questions.question_id"), index=True)
    participant: Mapped[str] = mapped_column(String(64))
    source_type: Mapped[str] = mapped_column(String(20), default="human")
    probability: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class OutcomeRecord(Base):
    __tablename__ = "outcomes"

    question_id: Mapped[str] = mapped_column(ForeignKey("forecast_questions.question_id"), primary_key=True)
    event_occurred: Mapped[bool] = mapped_column(Boolean)
    resolved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
