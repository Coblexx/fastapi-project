from typing import Any, Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.db import Base, get_db
from src.main import app
from src.models import Student as StudentModel
from src.schemas import StudentBase as StudentSchema

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


@pytest.fixture
def mock_student_model() -> StudentModel:
    return StudentModel(name="John Doe", age=21, email="john@example.com", major="Compsci")


@pytest.fixture
def mock_student_schema() -> StudentSchema:
    return StudentSchema(name="Jane Doe", age=21, email="jane@example.com", major="Compsci")


@pytest.fixture(autouse=True)
def setup_and_teardown(mock_student_model: StudentModel) -> Generator[Any, Any, Any]:
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    db.add(mock_student_model)
    db.commit()
    db.refresh(mock_student_model)

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


def test_create_student(mock_student_schema: StudentSchema) -> None:
    response = client.post(
        "/students/",
        json={**mock_student_schema.model_dump(), "age": 22},
    )
    assert response.status_code == 201
    assert response.json() == {"name": "Jane Doe", "email": "jane@example.com", "major": "Compsci"}


def test_conflict_create_student(mock_student_schema: StudentSchema) -> None:
    invalid_email_response = client.post(
        "/students/",
        json={**mock_student_schema.model_dump(), "email": "john@example.com"},
    )

    assert invalid_email_response.status_code == 409
    assert invalid_email_response.json() == {"detail": "Student with this email already exists"}


def test_read_student_by_id() -> None:
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "age": 21, "email": "john@example.com", "major": "Compsci"}


def test_invalid_read_student_by_id() -> None:
    response = client.get("/students/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}


def test_update_student(mock_student_schema: StudentSchema) -> None:
    response = client.put(
        "/students/1",
        json={**mock_student_schema.model_dump(), "name": "John Doe"},
    )

    assert response.status_code == 200
    assert response.json() == {"name": "John Doe", "email": "jane@example.com", "major": "Compsci"}


def test_update_invalid_student(mock_student_schema: StudentSchema) -> None:
    response = client.put(
        "/students/2",
        json={**mock_student_schema.model_dump()},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not found"}


def test_delete_student() -> None:
    response = client.delete("/students/1")
    assert response.status_code == 204


def test_delete_invalid_student() -> None:
    response = client.delete("/students/2")
    assert response.status_code == 204
