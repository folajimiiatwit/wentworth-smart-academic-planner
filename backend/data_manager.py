from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/"data"
REQUIRED_COURSES_FILE = DATA_DIR/"required_courses.csv"
SEMESTER_COURSES_FILE = DATA_DIR/"semester_courses.csv"
USERS_FILE = DATA_DIR/"users.csv"

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
    columns = ["username", "completed_required_courses"]+ELECTIVE_COLUMNS+["planned_courses"]
    if not USERS_FILE.exists():
        users = pd.DataFrame(columns=columns)
        users.to_csv(USER_FILE, index=False)

    users=pd.read_csv(USERS_FILE).fillna("")

    for column in columns:
        if column not in users.columns:
            if column in ELECTIVE_COLUMNS:
                users[column]=0
            else:
                ""
    return users[columns]
def save_users(users_df):
    users_df.to_csv(USERS_FILE, index=False)
def get_user(username):
    username=username.strip().lower()
    users=load_users()
    row=users[users["username"].astype(str).str.lower() == username]
    if row.empty:
        return None
    return row.iloc[0].to_dict()

def get_completed_required_courses(username):
    user= get_user(username)
    if user is None:
        return []
    completed_courses=user.get("completed_required_courses","")
    completed = str(completed_courses)
    if completed.strip()=="":
        return []
    for course in completed.split(";"):
        stripped_course=course.strip()
        if stripped_course:
            courses.append(stripped_course)
    return courses
        
def get_elective_credits(username):
    user=get_user(username)
    credits = {}
    for column in ELECTIVE_COLUMNS:
        if user is None:
            credits[column] = 0
        else:
            try:
                credits[column] = int(user.get(column,0))
            except ValueError:
                credits[column]=0
    return credits

def save_completed_info(username, completed_required_courses, elective_credit_data):
    username = username.strip().lower()
    users=load_users()
    index=users[ users["username"].astype(str).str.lower() == username ].index
    if len(index)==0:
        return False
    users.loc[index[0], "completed_required_courses"] = ";".join(completed_required_courses)

    for column in ELECTIVE_COLUMNS:
        users.loc[index[0],column]= int( elective_credit_data.get(column,0))
    save_users(users)
    return True
