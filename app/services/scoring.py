from __future__ import annotations

from collections import defaultdict

from app.models import ForecastSubmissionRecord, OutcomeRecord
from app.schemas import CalibrationPoint, ScoreRecord


def brier_score(probability: float, event_occurred: bool) -> float:
    outcome = 1.0 if event_occurred else 0.0
    return round((probability - outcome) ** 2, 6)


def compute_leaderboard(
    submissions: list[ForecastSubmissionRecord],
    outcomes_by_question: dict[str, OutcomeRecord],
) -> list[ScoreRecord]:
    buckets: dict[tuple[str, str], list[float]] = defaultdict(list)

    for sub in submissions:
        outcome = outcomes_by_question.get(sub.question_id)
        if not outcome:
            continue
        key = (sub.participant, sub.source_type)
        buckets[key].append(brier_score(sub.probability, outcome.event_occurred))

    rows: list[ScoreRecord] = []
    for (participant, source_type), scores in buckets.items():
        rows.append(
            ScoreRecord(
                participant=participant,
                source_type=source_type,
                mean_brier=round(sum(scores) / len(scores), 4),
                n=len(scores),
            )
        )
    return sorted(rows, key=lambda r: r.mean_brier)


def calibration_curve(
    submissions: list[ForecastSubmissionRecord],
    outcomes_by_question: dict[str, OutcomeRecord],
    bins: int = 5,
) -> list[CalibrationPoint]:
    bucket_values: dict[int, list[tuple[float, float]]] = defaultdict(list)

    for sub in submissions:
        outcome = outcomes_by_question.get(sub.question_id)
        if not outcome:
            continue
        b = min(bins - 1, int(sub.probability * bins))
        bucket_values[b].append((sub.probability, 1.0 if outcome.event_occurred else 0.0))

    result: list[CalibrationPoint] = []
    for b in range(bins):
        low = b / bins
        high = (b + 1) / bins
        entries = bucket_values.get(b, [])
        if entries:
            predicted_mean = sum(p for p, _ in entries) / len(entries)
            observed_rate = sum(o for _, o in entries) / len(entries)
            count = len(entries)
        else:
            predicted_mean = 0.0
            observed_rate = 0.0
            count = 0
        result.append(
            CalibrationPoint(
                bin_lower=round(low, 2),
                bin_upper=round(high, 2),
                predicted_mean=round(predicted_mean, 4),
                observed_rate=round(observed_rate, 4),
                count=count,
            )
        )
    return result
