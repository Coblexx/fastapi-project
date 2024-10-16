from typing import Any, Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.db import Base, get_db
from src.main import app
from src.models import Student as StudentModel

client = TestClient(app)


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_and_teardown() -> Generator[Any, Any, Any]:
    Base.metadata.create_all(bind=engine)

    mocked_student = StudentModel(name="John Doe", age=21, email="john@example.com", major="Compsci")
    db = TestingSessionLocal()
    db.add(mocked_student)
    db.commit()
    db.refresh(mocked_student)

    yield
    Base.metadata.drop_all(bind=engine)


def test_read_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_students() -> None:
    response = client.get("/students/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "John Doe", "age": 21, "email": "john@example.com", "major": "Compsci"}
    ]


def test_create_student() -> None:
    mock_student = {"name": "Jane Doe", "age": 22, "email": "jane@example.com", "major": "Compsci"}

    response = client.post(
        "/students/",
        json=mock_student,
    )
    assert response.status_code == 201
    assert response.json() == {"name": "Jane Doe", "email": "jane@example.com", "major": "Compsci"}


def test_conflict_create_student() -> None:
    mock_student_conflict_email = {"name": "Jane Doe", "age": 22, "email": "john@example.com", "major": "Compsci"}

    invalid_email_response = client.post(
        "/students/",
        json=mock_student_conflict_email,
    )

    assert invalid_email_response.status_code == 400
    assert invalid_email_response.json() == {
        "detail": "An error occurred while creating student: 400: Student could not have been created!"
    }


def test_read_student_by_id() -> None:
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "age": 21, "email": "john@example.com", "major": "Compsci"}


def test_invalid_read_student_by_id() -> None:
    response = client.get("/students/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "An error occured while fetching student data: 404: Student not found"}


def test_update_student() -> None:
    mock_update = {"name": "Jane Doe", "age": 22, "email": "jane@example.com", "major": "Compsci"}

    response = client.put(
        "/students/1",
        json=mock_update,
    )

    assert response.status_code == 200
    assert response.json() == {"name": "Jane Doe", "email": "jane@example.com", "major": "Compsci"}


def test_delete_student() -> None:
    response = client.delete("/students/1")
    assert response.status_code == 204
