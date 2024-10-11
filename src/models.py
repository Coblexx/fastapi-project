from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    age: int
    email: str | None = None


class Student(StudentBase):
    student_id: int


class StudentBaseOut(BaseModel):
    name: str
    email: str | None = None


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    email: str | None = None
