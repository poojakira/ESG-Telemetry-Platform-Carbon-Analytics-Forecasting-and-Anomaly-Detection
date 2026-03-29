from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.auth import get_current_user
from app.db import get_db
import pytest


def override_get_current_user():
    """Return a mock admin user for CI testing."""
    user = MagicMock()
    user.username = "ci_test_user"
    user.role = "admin"
    return user


def override_get_db():
    """Yield a real in-memory SQLite session for CI testing."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.db import Base

    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db
