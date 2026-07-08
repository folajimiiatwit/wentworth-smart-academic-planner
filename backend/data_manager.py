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

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

REQUIRED_COURSES_FILE = DATA_DIR / "cs_required_courses.csv"
SEMESTER_COURSES_FILE = DATA_DIR / "semester_courses.csv"
USERS_FILE = DATA_DIR / "users.csv"

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


def load_users():
    """
    Load saved user progress data and create the users file if it does not exist.

    This function ensures that all expected user-progress columns are present,
    including completed required courses, custom completed courses, elective credit
    categories, and planned courses.

    Returns:
        pandas.DataFrame: User records with all required columns included.
    """
    columns = ["username", "completed_required_courses", "custom_completed_courses"] + ELECTIVE_COLUMNS + ["planned_courses"]

    if not USERS_FILE.exists():
        users = pd.DataFrame(columns=columns)
        users.to_csv(USERS_FILE, index=False)

    users = pd.read_csv(USERS_FILE).fillna("")

    for column in columns:
        if column not in users.columns:
            users[column] = 0 if column in ELECTIVE_COLUMNS else ""

    return users[columns]


def save_users(users_df):
    """
    Save the full users DataFrame back to the users CSV file.

    Args:
        users_df (pandas.DataFrame): Updated user records to persist.
    """
    users_df.to_csv(USERS_FILE, index=False)


def get_user(username):
    """
    Retrieve a single user record by username.

    The username is normalized before lookup so that matching is case-insensitive.

    Args:
        username (str): Username to search for.

    Returns:
        dict | None: User record as a dictionary, or None if the user is not found.
    """
    username = username.strip().lower()
    users = load_users()
    row = users[users["username"].astype(str).str.lower() == username]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def get_completed_required_courses(username):
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
    completed = str(user.get("completed_required_courses", ""))
    if completed.strip() == "":
        return []
    return [course.strip() for course in completed.split(";") if course.strip()]


def get_custom_completed_courses(username):
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

    completed = str(user.get("custom_completed_courses", ""))
    if completed.strip() == "":
        return []

    custom_courses = []
    for item in completed.split(";"):
        parts = item.split("|")
        if len(parts) >= 3:
            custom_courses.append({
                "course_code": parts[0].strip(),
                "course_number": parts[1].strip(),
                "title": parts[2].strip()
            })

    return custom_courses


def get_all_completed_course_codes(username):
    """
    Combine required and custom completed course codes for prerequisite checking.

    Args:
        username (str): Username whose completed courses should be retrieved.

    Returns:
        list[str]: All completed course codes for the user.
    """
    required_courses = get_completed_required_courses(username)
    custom_courses = get_custom_completed_courses(username)
    custom_codes = [course["course_code"] for course in custom_courses]
    return required_courses + custom_codes


def save_custom_completed_courses(username, custom_courses):
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
    username = username.strip().lower()
    users = load_users()

    index = users[users["username"].astype(str).str.lower() == username].index

    if len(index) == 0:
        return False

    encoded_courses = []
    for course in custom_courses:
        course_code = str(course.get("course_code", "")).strip().upper()
        course_number = str(course.get("course_number", "")).strip()
        title = str(course.get("title", "")).strip()

        if course_code:
            encoded_courses.append(f"{course_code}|{course_number}|{title}")

    users.loc[index[0], "custom_completed_courses"] = ";".join(encoded_courses)
    save_users(users)
    return True


def get_elective_credits(username):
    """
    Load the user's completed elective credit totals by category.

    Args:
        username (str): Username whose elective credits should be loaded.

    Returns:
        dict: Elective credit category names mapped to integer credit totals.
    """
    user = get_user(username)
    credits = {}

    for column in ELECTIVE_COLUMNS:
        if user is None:
            credits[column] = 0
        else:
            try:
                credits[column] = int(user.get(column, 0))
            except ValueError:
                credits[column] = 0

    return credits


def save_completed_info(username, completed_required_courses, elective_credit_data):
    """
    Save completed required courses and elective credit totals for a user.

    Args:
        username (str): Username whose progress should be updated.
        completed_required_courses (list[str]): Required course codes completed by the user.
        elective_credit_data (dict): Elective credit totals by category.

    Returns:
        bool: True if the user was found and saved; False otherwise.
    """
    username = username.strip().lower()
    users = load_users()
    index = users[users["username"].astype(str).str.lower() == username].index

    if len(index) == 0:
        return False

    users.loc[index[0], "completed_required_courses"] = ";".join(completed_required_courses)

    for column in ELECTIVE_COLUMNS:
        users.loc[index[0], column] = int(elective_credit_data.get(column, 0))

    save_users(users)
    return True
