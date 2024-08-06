from typing import Generator
from fastapi.testclient import TestClient
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import pytest
from sqlalchemy.orm import Session

from src.database import get_db
from src.rest_api import app

@pytest.fixture
def mock_db() -> Generator[Session, None, None]:
    db = UnifiedAlchemyMagicMock()
    yield db

@pytest.fixture
def rest_client(mock_db: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: mock_db
    client = TestClient(app)
    yield client
