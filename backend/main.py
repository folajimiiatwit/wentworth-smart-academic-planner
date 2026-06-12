from fastapi import FastAPI
from backend.models import LoginRequest,CompletedCoursesRequest, ScheduleCheckRequest, CustomCompletedCoursesRequest
from backend.auth import login_user
from backend.data_manager import (load_required_courses, load_semester_courses, get_completed_required_courses, get_custom_completed_courses, get_all_completed_course_codes, get_elective_credits,save_completed_info,save_custom_completed_courses)
from backend.planner import (add_course_groups,get_eligible_semester_courses,get_blocked_semester_courses,required_progress,check_schedule)

app = FastAPI(title="Wentworth Smart Planner")

@app.get("/health")
def health_check():
    return {"status": "running"}


@app.post("/login")
def login(request: LoginRequest):
    return login_user(request.username)


@app.get("/required-courses")
def required_courses():
    required_df = add_course_groups(load_required_courses())
    return required_df.to_dict(orient="records")


@app.get("/semester-courses")
def semester_courses():
    semester_df = add_course_groups(load_semester_courses())
    return semester_df.to_dict(orient="records")


@app.get("/completed-info/{username}")
def completed_info(username: str):
    return {
        "username": username,
        "completed_required_courses": get_completed_required_courses(username),
        "custom_completed_courses": get_custom_completed_courses(username),
        "elective_credits": get_elective_credits(username)
    }


@app.post("/save-completed-info")
def save_completed(request: CompletedCoursesRequest):
    elective_data = {
        "general_elective_credits": request.general_elective_credits,
        "cs_elective_credits": request.cs_elective_credits,
        "english_elective_credits": request.english_elective_credits,
        "science_elective_credits": request.science_elective_credits,
        "humanities_elective_credits": request.humanities_elective_credits,
        "social_science_elective_credits": request.social_science_elective_credits,
        "ethics_elective_credits": request.ethics_elective_credits
    }

    save_completed_info(request.username, request.completed_required_courses, elective_data)
    return {"message": "Completed information saved"}


@app.post("/save-custom-completed")
def save_custom_completed(request: CustomCompletedCoursesRequest):
    custom_courses = [
        course.dict()
        for course in request.custom_completed_courses
    ]

    save_custom_completed_courses(request.username, custom_courses)
    return {"message": "Custom completed courses saved"}


@app.get("/eligible-courses/{username}")
def eligible_courses(username: str):
    semester_df = load_semester_courses()
    completed = get_all_completed_course_codes(username)
    eligible = get_eligible_semester_courses(semester_df, completed)
    return eligible.to_dict(orient="records")


@app.get("/blocked-courses/{username}")
def blocked_courses(username: str):
    semester_df = load_semester_courses()
    completed = get_all_completed_course_codes(username)
    return get_blocked_semester_courses(semester_df, completed)


@app.get("/progress/{username}")
def progress(username: str):
    required_df = load_required_courses()
    completed = get_completed_required_courses(username)
    elective_credits = get_elective_credits(username)
    return required_progress(required_df, completed, elective_credits)


@app.post("/check-schedule")
def check_selected_schedule(request: ScheduleCheckRequest):
    semester_df = load_semester_courses()
    return check_schedule(semester_df, request.selected_courses)

