from datetime import datetime
import re

ELECTIVE_REQUIREMENTS = {
    "general_elective_credits": 8,
    "cs_elective_credits": 16,
    "english_elective_credits": 8,
    "science_elective_credits": 8,
    "humanities_elective_credits": 4,
    "social_science_elective_credits": 4,
    "ethics_elective_credits": 4
}
def get_course_group(course_code):

def add_course_groups(df):

def clean_course_code(course_code):

def evaluate_prerequisite_rule(prerequisite_text, completed_courses):

def missing_prerequisites(prerequisite_text, completed_courses):

def get_eligible_semester_courses(semester_courses_df, completed_courses):

def get_blocked_semester_courses(semester_courses_df, completed_courses):

def elective_progress(elective_credits):

def required_progress(required_courses_df, completed_required_courses, elective_credits):

def time_to_minutes(time_text):

def days_overlap(days_1, days_2):

def courses_conflict(course_1, course_2):

def find_conflicts(selected_courses_df):

def check_schedule(semester_courses_df, selected_course_sections):
