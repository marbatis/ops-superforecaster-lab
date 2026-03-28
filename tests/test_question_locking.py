from datetime import datetime, timedelta, timezone

from app.models import ForecastQuestionRecord
from app.repositories.forecast_repo import ForecastRepository
from app.services.forecasting import lock_expired_questions


def test_lock_expired_question(db_session) -> None:
    repo = ForecastRepository(db_session)
    repo.create_question(
        ForecastQuestionRecord(
            question_id="q_expired",
            target_type="cpu_spike_probability",
            question_text="expired",
            deadline=datetime.now(timezone.utc) - timedelta(days=1),
            status="active",
        )
    )
    lock_expired_questions(repo)
    assert repo.get_question("q_expired").status == "locked"
