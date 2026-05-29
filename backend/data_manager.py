from pathlib import Path
import pandas as pd
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

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

def load_semester_courses():

def load_users():

def save_users(users_df):

def get_user(username):

def get_completed_required_courses(username):

def get_elective_credits(username):

def save_completed_info(username, completed_required_courses, elective_credit_data):
