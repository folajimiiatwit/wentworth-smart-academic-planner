"""
Purpose:
Handles reading and writing application data.

Main responsibilities:
- Load required course data
- Load semester course offerings
- Load and update user progress
- Save completed required courses
- Save custom completed courses
- Save elective credit information
"""
from pathlib import Path
import pandas as pd

from sqlalchemy import select

from backend.database import SessionLocal
from backend.database_models import User

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

REQUIRED_COURSES_FILE = DATA_DIR / "cs_required_courses.csv"
SEMESTER_COURSES_FILE = DATA_DIR / "semester_courses.csv"

ELECTIVE_COLUMNS = [
    "general_elective_credits",
    "cs_elective_credits",
    "english_elective_credits",
    "science_elective_credits",
    "humanities_elective_credits",
    "social_science_elective_credits",
    "ethics_elective_credits"
]


def load_required_courses():
    """
    Load the required Computer Science course list from the required-courses CSV file.

    Returns:
        pandas.DataFrame: Required course records with missing values replaced by
        empty strings.
    """
    return pd.read_csv(REQUIRED_COURSES_FILE).fillna("")


def load_semester_courses():
    """
    Load the available semester course offerings from the semester-courses CSV file.

    Returns:
        pandas.DataFrame: Semester course records with missing values replaced by
        empty strings.
    """
    return pd.read_csv(SEMESTER_COURSES_FILE).fillna("")


def normalize_username(username: str) -> str:
    """
    Normalize a username before database storage or lookup.
    """
    return username.strip().lower()

def get_user(username):
    """
    Retrieve a single user record by username.

    The username is normalized before lookup so that matching is case-insensitive.

    Args:
        username (str): Username to search for.

    Returns:
        dict | None: Database user record, or None if not found.
    """
    normalized_username = normalize_username(username)

    with SessionLocal() as database:
        statement = select(User).where(
            User.username == normalized_username
        )

        return database.scalar(statement)

def create_user(username: str):
    """
    Create a database user if the username does not already exist.

    Args:
        username: Username to create.

    Returns:
        User | None: The existing or newly created user.
    """
    normalized_username = normalize_username(username)

    if not normalized_username:
        return None

    with SessionLocal() as database:
        existing_user = database.scalar(
            select(User).where(
                User.username == normalized_username
            )
        )

        if existing_user is not None:
            return existing_user

        new_user = User(
            username=normalized_username
        )

        database.add(new_user)
        database.commit()
        database.refresh(new_user)

        return new_user

def get_completed_required_courses(username: str) -> list[str]:
    """
    Return the list of required courses completed by a user.

    Completed courses are stored as a semicolon-separated string in the users CSV
    file and are converted back into a Python list.

    Args:
        username (str): Username whose completed required courses should be loaded.

    Returns:
        list[str]: Completed required course codes.
    """
    user = get_user(username)

    if user is None:
        return []

    completed = user.completed_required_courses or ""

    return [
        course.strip()
        for course in completed.split(";")
        if course.strip()
    ]

def get_custom_completed_courses(username: str) -> list[dict]:
    """
    Return the list of custom or transfer courses completed by a user.

    Custom courses are stored as encoded strings using the format
    `course_code|course_number|title` and are converted into dictionaries for use by
    the frontend.

    Args:
        username (str): Username whose custom completed courses should be loaded.

    Returns:
        list[dict]: Custom completed course records.
    """
    user = get_user(username)

    if user is None:
        return []

    completed = user.custom_completed_courses or ""

    if not completed.strip():
        return []

    custom_courses = []

    for item in completed.split(";"):
        parts = item.split("|")

        if len(parts) >= 3:
            custom_courses.append(
                {
                    "course_code": parts[0].strip(),
                    "course_number": parts[1].strip(),
                    "title": "|".join(parts[2:]).strip(),
                }
            )

    return custom_courses


def get_all_completed_course_codes(username: str) -> list[str]:
    """
    Combine required and custom completed course codes for prerequisite checking.

    Args:
        username (str): Username whose completed courses should be retrieved.

    Returns:
        list[str]: All completed course codes for the user.
    """
    required_courses = get_completed_required_courses(username)
    custom_courses = get_custom_completed_courses(username)

    custom_codes = [
        course["course_code"]
        for course in custom_courses
    ]

    return required_courses + custom_codes


def save_custom_completed_courses(
        username: str,
        custom_courses: list[dict],
    ) -> bool:
    """
    Save a user's custom or transfer completed courses.

    Each custom course is encoded as `course_code|course_number|title` before being
    stored in the users CSV file.

    Args:
        username (str): Username whose custom courses should be updated.
        custom_courses (list[dict]): Custom course records from the frontend.

    Returns:
        bool: True if the user was found and saved; False otherwise.
    """
    normalized_username = normalize_username(username)

    with SessionLocal() as database:
        user = database.scalar(
            select(User).where(
                User.username == normalized_username
            )
        )

        if user is None:
            return False

        encoded_courses = []

        for course in custom_courses:
            course_code = str(
                course.get("course_code", "")
            ).strip().upper()

            course_number = str(
                course.get("course_number", "")
            ).strip()

            title = str(
                course.get("title", "")
            ).strip()

            if course_code:
                encoded_courses.append(
                    f"{course_code}|{course_number}|{title}"
                )

        user.custom_completed_courses = ";".join(
            encoded_courses
        )

        database.commit()

        return True


def get_elective_credits(username: str) -> dict[str, int]:
    """
    Load the user's completed elective credit totals by category.

    Args:
        username (str): Username whose elective credits should be loaded.

    Returns:
        dict: Elective credit category names mapped to integer credit totals.
    """
    user = get_user(username)

    if user is None:
        return {
            column: 0
            for column in ELECTIVE_COLUMNS
        }

    credits = {}

    for column in ELECTIVE_COLUMNS:
        value = getattr(user, column, 0)

        try:
            credits[column] = int(value or 0)
        except (TypeError, ValueError):
            credits[column] = 0

    return credits


def save_completed_info(
        username: str,
        completed_required_courses: list[str],
        elective_credit_data: dict,
    ) -> bool:
    """
    Save completed required courses and elective credit totals for a user.

    Args:
        username (str): Username whose progress should be updated.
        completed_required_courses (list[str]): Required course codes completed by the user.
        elective_credit_data (dict): Elective credit totals by category.

    Returns:
        bool: True if the user was found and saved; False otherwise.
    """
    normalized_username = normalize_username(username)

    with SessionLocal() as database:
        user = database.scalar(
            select(User).where(
                User.username == normalized_username
            )
        )

        if user is None:
            return False

        cleaned_courses = [
            str(course).strip().upper()
            for course in completed_required_courses
            if str(course).strip()
        ]

        user.completed_required_courses = ";".join(
            cleaned_courses
        )

        for column in ELECTIVE_COLUMNS:
            value = elective_credit_data.get(column, 0)

            try:
                value = int(value)
            except (TypeError, ValueError):
                value = 0

            setattr(
                user,
                column,
                max(value, 0),
            )

        database.commit()

        return True

