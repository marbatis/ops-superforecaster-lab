from app.repositories.forecast_repo import ForecastRepository
from app.services.forecasting import record_outcome, submit_forecast
from app.services.leaderboard import build_score_views


def test_leaderboard_updates(db_session) -> None:
    repo = ForecastRepository(db_session)
    submit_forecast(repo, "q_batch_miss", "alice", 0.7, "human")
    record_outcome(repo, "q_batch_miss", True)

    views = build_score_views(repo)
    assert views["leaderboard"]
    assert "mean_brier" in views["leaderboard"][0]
