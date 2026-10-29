import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

import app.services.task as task_service
from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.models.task import Task

TEST_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database="task_tracker_test",
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def client(monkeypatch):
    Base.metadata.create_all(test_engine)

    monkeypatch.setattr(
        task_service,
        "SessionLocal",
        TestingSessionLocal,
    )

    with TestingSessionLocal() as db:
        db.query(Task).delete()
        db.commit()

    with TestClient(app) as test_client:
        yield test_client
