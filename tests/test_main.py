from typing import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from src.core.db import Base, get_db
from src.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db() -> Generator[Session, None, None]:
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    inspector = inspect(test_engine)
    tables = inspector.get_table_names()

    print(tables)
    assert "students" in tables, f"Table 'students' not found in {tables}"
    print("TestSession")
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    db = TestSession()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(test_db: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_student(client: TestClient) -> None:
    response = client.post(
        "/students/",
        json={"name": "John Doe", "age": 21, "email": None},
    )
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "John Doe", "age": 21, "email": None}
