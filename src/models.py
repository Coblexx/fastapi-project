from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True, default=None)
    major: Mapped[str] = mapped_column(String, nullable=True, default=None)
