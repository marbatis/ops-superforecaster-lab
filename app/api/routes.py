from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.forecast_repo import ForecastRepository
from app.schemas import ForecastSubmissionIn, OutcomeIn
from app.services.forecasting import (
    baseline_probability,
    lock_expired_questions,
    model_probability,
    record_outcome,
    submit_forecast,
)
from app.services.leaderboard import build_score_views

router = APIRouter(prefix="/api", tags=["api"])


def _repo(db: Session) -> ForecastRepository:
    return ForecastRepository(db)


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/questions")
def list_questions(db: Session = Depends(get_db)) -> dict:
    repo = _repo(db)
    lock_expired_questions(repo)
    rows = repo.list_questions()
    return {"questions": rows}


@router.post("/questions/{question_id}/forecast")
def submit(question_id: str, body: ForecastSubmissionIn, db: Session = Depends(get_db)) -> dict:
    repo = _repo(db)
    lock_expired_questions(repo)
    ok, msg = submit_forecast(repo, question_id, body.participant, body.probability, body.source_type)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": msg}


@router.post("/questions/{question_id}/baseline")
def submit_baseline(question_id: str, db: Session = Depends(get_db)) -> dict:
    repo = _repo(db)
    question = repo.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    submit_forecast(repo, question_id, "baseline", baseline_probability(question.target_type), "baseline")
    submit_forecast(repo, question_id, "model", model_probability(question.target_type), "model")
    return {"status": "baseline/model submitted"}


@router.post("/questions/{question_id}/resolve")
def resolve(question_id: str, body: OutcomeIn, db: Session = Depends(get_db)) -> dict:
    repo = _repo(db)
    ok, msg = record_outcome(repo, question_id, body.event_occurred)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": msg}


@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)) -> dict:
    return build_score_views(_repo(db))


@router.get("/calibration")
def calibration(db: Session = Depends(get_db)) -> dict:
    return {"calibration": build_score_views(_repo(db))["calibration"]}
