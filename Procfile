release: python -c "from app.db import init_db, SessionLocal; init_db(); from app.repositories.forecast_repo import ForecastRepository; from app.services.questions import seed_questions; db = SessionLocal(); seed_questions(ForecastRepository(db)); db.close()"
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
