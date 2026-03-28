from __future__ import annotations

from app.repositories.forecast_repo import ForecastRepository
from app.services.scoring import calibration_curve, compute_leaderboard


def build_score_views(repo: ForecastRepository) -> dict:
    submissions = repo.list_submissions()
    outcomes = {item.question_id: item for item in repo.list_outcomes()}

    leaderboard = compute_leaderboard(submissions, outcomes)
    calibration = calibration_curve(submissions, outcomes)

    return {
        "leaderboard": [item.model_dump(mode="json") for item in leaderboard],
        "calibration": [item.model_dump(mode="json") for item in calibration],
    }
