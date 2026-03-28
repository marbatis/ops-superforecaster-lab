from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models import ForecastQuestionRecord
from app.repositories.forecast_repo import ForecastRepository

SAMPLE_QUESTIONS = [
    {
        "question_id": "q_batch_miss",
        "target_type": "batch_miss_probability",
        "question_text": "Will nightly billing batch miss SLA this week?",
    },
    {
        "question_id": "q_cpu_spike",
        "target_type": "cpu_spike_probability",
        "question_text": "Will API CPU exceed 90% for >10 minutes this week?",
    },
    {
        "question_id": "q_incident_recur",
        "target_type": "incident_recurrence_probability",
        "question_text": "Will auth incident type INC-472 recur within 14 days?",
    },
]


def seed_questions(repo: ForecastRepository) -> None:
    if repo.list_questions():
        return

    deadline = datetime.now(timezone.utc) + timedelta(days=7)
    for item in SAMPLE_QUESTIONS:
        repo.create_question(
            ForecastQuestionRecord(
                question_id=item["question_id"],
                target_type=item["target_type"],
                question_text=item["question_text"],
                deadline=deadline,
                status="active",
            )
        )
