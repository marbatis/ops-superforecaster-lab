from __future__ import annotations

from collections.abc import Generator
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.models import Base

_engine: Optional[Engine] = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def configure_database(url: str) -> None:
    global _engine
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    _engine = create_engine(url, connect_args=connect_args)
    SessionLocal.configure(bind=_engine)


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        configure_database(get_settings().database_url)
    return _engine  # type: ignore[return-value]


def init_db() -> None:
    Base.metadata.create_all(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
