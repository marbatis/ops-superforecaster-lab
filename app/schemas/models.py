from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ForecastQuestion(BaseModel):
    question_id: str
    target_type: str
    question_text: str
    deadline: datetime
    status: str


class ForecastSubmissionIn(BaseModel):
    participant: str
    probability: float = Field(ge=0.0, le=1.0)
    source_type: str = "human"


class OutcomeIn(BaseModel):
    event_occurred: bool


class ScoreRecord(BaseModel):
    participant: str
    source_type: str
    mean_brier: float
    n: int


class CalibrationPoint(BaseModel):
    bin_lower: float
    bin_upper: float
    predicted_mean: float
    observed_rate: float
    count: int
