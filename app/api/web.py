from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.forecast_repo import ForecastRepository
from app.services.forecasting import lock_expired_questions
from app.services.leaderboard import build_score_views

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def active_questions(request: Request, db: Session = Depends(get_db)):
    repo = ForecastRepository(db)
    lock_expired_questions(repo)
    questions = repo.list_questions(status="active")
    return templates.TemplateResponse("index.html", {"request": request, "questions": questions})


@router.get("/resolved")
def resolved_questions(request: Request, db: Session = Depends(get_db)):
    repo = ForecastRepository(db)
    questions = repo.list_questions(status="resolved")
    return templates.TemplateResponse("resolved.html", {"request": request, "questions": questions})


@router.get("/leaderboard")
def leaderboard_page(request: Request, db: Session = Depends(get_db)):
    views = build_score_views(ForecastRepository(db))
    return templates.TemplateResponse("leaderboard.html", {"request": request, **views})
