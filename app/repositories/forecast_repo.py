from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import ForecastQuestionRecord, ForecastSubmissionRecord, OutcomeRecord


class ForecastRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_question(self, question: ForecastQuestionRecord) -> None:
        self.db.add(question)
        self.db.commit()

    def list_questions(self, status: str | None = None) -> list[ForecastQuestionRecord]:
        stmt = select(ForecastQuestionRecord)
        if status:
            stmt = stmt.where(ForecastQuestionRecord.status == status)
        return list(self.db.scalars(stmt.order_by(ForecastQuestionRecord.deadline)).all())

    def get_question(self, question_id: str) -> ForecastQuestionRecord | None:
        return self.db.scalar(select(ForecastQuestionRecord).where(ForecastQuestionRecord.question_id == question_id))

    def upsert_submission(self, submission: ForecastSubmissionRecord) -> None:
        existing = self.db.scalar(
            select(ForecastSubmissionRecord).where(
                and_(
                    ForecastSubmissionRecord.question_id == submission.question_id,
                    ForecastSubmissionRecord.participant == submission.participant,
                    ForecastSubmissionRecord.source_type == submission.source_type,
                )
            )
        )
        if existing:
            existing.probability = submission.probability
            existing.created_at = datetime.now(timezone.utc)
        else:
            self.db.add(submission)
        self.db.commit()

    def list_submissions(self) -> list[ForecastSubmissionRecord]:
        return list(self.db.scalars(select(ForecastSubmissionRecord)).all())

    def list_submissions_for_question(self, question_id: str) -> list[ForecastSubmissionRecord]:
        return list(
            self.db.scalars(
                select(ForecastSubmissionRecord).where(ForecastSubmissionRecord.question_id == question_id)
            ).all()
        )

    def upsert_outcome(self, outcome: OutcomeRecord) -> None:
        existing = self.db.scalar(select(OutcomeRecord).where(OutcomeRecord.question_id == outcome.question_id))
        if existing:
            existing.event_occurred = outcome.event_occurred
            existing.resolved_at = outcome.resolved_at
        else:
            self.db.add(outcome)

        question = self.get_question(outcome.question_id)
        if question:
            question.status = "resolved"
        self.db.commit()

    def get_outcome(self, question_id: str) -> OutcomeRecord | None:
        return self.db.scalar(select(OutcomeRecord).where(OutcomeRecord.question_id == question_id))

    def list_outcomes(self) -> list[OutcomeRecord]:
        return list(self.db.scalars(select(OutcomeRecord)).all())
