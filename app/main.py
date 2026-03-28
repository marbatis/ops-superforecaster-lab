from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import api_router, web_router
from app.db import init_db
from app.logging_config import configure_logging
from app.repositories.forecast_repo import ForecastRepository
from app.services.questions import seed_questions

configure_logging()
app = FastAPI(title="Ops Superforecaster Lab", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(web_router)
app.include_router(api_router)


@app.on_event("startup")
def startup() -> None:
    init_db()
    from app.db import SessionLocal

    db = SessionLocal()
    try:
        seed_questions(ForecastRepository(db))
    finally:
        db.close()
