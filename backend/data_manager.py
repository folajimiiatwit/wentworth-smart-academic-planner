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
    return pd.read_csv(REQUIRED_COURSES_FILE).fillna("")


def load_semester_courses():
    return pd.read_csv(SEMESTER_COURSES_FILE).fillna("")


def load_users():
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
    users_df.to_csv(USERS_FILE, index=False)


def get_user(username):
    username = username.strip().lower()
    users = load_users()
    row = users[users["username"].astype(str).str.lower() == username]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def get_completed_required_courses(username):
    user = get_user(username)
    if user is None:
        return []
    completed = str(user.get("completed_required_courses", ""))
    if completed.strip() == "":
        return []
    return [course.strip() for course in completed.split(";") if course.strip()]


def get_custom_completed_courses(username):
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
    required_courses = get_completed_required_courses(username)
    custom_courses = get_custom_completed_courses(username)
    custom_codes = [course["course_code"] for course in custom_courses]
    return required_courses + custom_codes


def save_custom_completed_courses(username, custom_courses):
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
