from app.services.scoring import brier_score


def test_brier_score() -> None:
    assert brier_score(0.8, True) == 0.04
    assert brier_score(0.2, False) == 0.04
