# Task Environment

## 1. Rational objective
Compare operational forecasts across human, baseline, and model-assisted sources using proper scoring.

## 2. PEAS
- Performance: Brier score quality, calibration, leaderboard transparency.
- Environment: synthetic operational forecast questions.
- Actuators: score computation and ranking.
- Sensors: forecast submissions and resolved outcomes.

## 3. Environmental dimensions
Time-bounded, uncertain outcomes, and sparse data per question.

## 4. Problem formalization
Given probability forecasts and outcomes, compute Brier scores and calibration by participant/source.

## 5. Architecture choice
FastAPI + SQLAlchemy with deterministic scoring modules.

## 6. Guardrails / workflow maturity
No hidden authority, explicit uncertainty, and immutable resolved outcomes.
