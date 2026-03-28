from __future__ import annotations

from datetime import datetime, timezone

from app.models import ForecastSubmissionRecord, OutcomeRecord
from app.repositories.forecast_repo import ForecastRepository


def _as_naive_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def baseline_probability(target_type: str) -> float:
    defaults = {
        "batch_miss_probability": 0.25,
        "cpu_spike_probability": 0.35,
        "incident_recurrence_probability": 0.3,
    }
    return defaults.get(target_type, 0.3)


def model_probability(target_type: str) -> float:
    hints = {
        "batch_miss_probability": 0.32,
        "cpu_spike_probability": 0.41,
        "incident_recurrence_probability": 0.28,
    }
    return hints.get(target_type, 0.33)


def submit_forecast(
    repo: ForecastRepository,
    question_id: str,
    participant: str,
    probability: float,
    source_type: str,
) -> tuple[bool, str]:
    question = repo.get_question(question_id)
    if not question:
        return False, "Question not found"

    now = _as_naive_utc(datetime.now(timezone.utc))
    deadline = _as_naive_utc(question.deadline)
    if question.status != "active" or now > deadline:
        return False, "Question is locked"

    repo.upsert_submission(
        ForecastSubmissionRecord(
            question_id=question_id,
            participant=participant,
            source_type=source_type,
            probability=probability,
        )
    )
    return True, "submitted"


def lock_expired_questions(repo: ForecastRepository) -> None:
    now = _as_naive_utc(datetime.now(timezone.utc))
    changed = False
    for question in repo.list_questions(status="active"):
        if _as_naive_utc(question.deadline) < now:
            question.status = "locked"
            changed = True
    if changed:
        repo.db.commit()


def record_outcome(repo: ForecastRepository, question_id: str, event_occurred: bool) -> tuple[bool, str]:
    question = repo.get_question(question_id)
    if not question:
        return False, "Question not found"

    repo.upsert_outcome(
        OutcomeRecord(
            question_id=question_id,
            event_occurred=event_occurred,
            resolved_at=datetime.now(timezone.utc),
        )
    )
    return True, "resolved"
