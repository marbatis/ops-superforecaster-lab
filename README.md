# ops-superforecaster-lab

Operational forecasting lab with Brier scoring, calibration, and leaderboard views.

## Overview
Users submit probability forecasts for operational events, outcomes are recorded, and performance is scored transparently.

## Forecast targets
- batch miss probability
- CPU spike probability
- incident recurrence probability

## Architecture
- Questions: `app/services/questions.py`
- Forecasting workflow: `app/services/forecasting.py`
- Scoring: `app/services/scoring.py`
- Leaderboard/calibration: `app/services/leaderboard.py`

## Local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Core API
- `POST /api/questions/{question_id}/forecast`
- `POST /api/questions/{question_id}/resolve`
- `GET /api/leaderboard`
- `GET /api/calibration`

## Heroku
`Procfile` and `runtime.txt` are included.
