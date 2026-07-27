from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class User(Base):
    """Saved account and academic-progress information."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    completed_required_courses: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    custom_completed_courses: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    general_elective_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    cs_elective_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    english_elective_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    science_elective_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    humanities_elective_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    social_science_elective_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    ethics_elective_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    planned_courses: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )