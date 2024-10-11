from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class Student(Base):  # type: ignore
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True, default=None)
    major: Mapped[str] = mapped_column(String, nullable=True, default=None)
