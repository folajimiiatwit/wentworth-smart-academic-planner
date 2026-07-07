"""
Purpose:
This provides helper functions for formatting and organizing course data.

Main responsibilities:
- Group courses by subject or category
- Create unique course section identifiers
- Format course labels for display in the schedule builder
"""
import requests
import subprocess
import sys
import time

API_URL = "http://127.0.0.1:8000"

def ensure_backend_running():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=2
        )

        if response.status_code == 200:
            return

    except Exception:
        pass

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000"
        ]
    )

    for _ in range(20):
        try:
            response = requests.get(
                f"{API_URL}/health",
                timeout=2
            )

            if response.status_code == 200:
                return

        except Exception:
            pass

        time.sleep(0.5)
        
def api_available():
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def login_user(username):
    return requests.post(
        f"{API_URL}/login",
        json={"username": username}
    )


def get_completed_info(username):
    return requests.get(f"{API_URL}/completed-info/{username}")


def get_required_courses():
    return requests.get(f"{API_URL}/required-courses")


def upload_transcript(uploaded_file):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    return requests.post(
        f"{API_URL}/parse-transcript",
        files=files
    )


def save_completed_info(username, completed_required_courses, elective_data):
    payload = {
        "username": username,
        "completed_required_courses": completed_required_courses,
        **elective_data
    }

    return requests.post(
        f"{API_URL}/save-completed-info",
        json=payload
    )


def save_custom_completed(username, custom_completed_courses):
    return requests.post(
        f"{API_URL}/save-custom-completed",
        json={
            "username": username,
            "custom_completed_courses": custom_completed_courses
        }
    )


def get_progress(username):
    return requests.get(f"{API_URL}/progress/{username}")


def get_eligible_courses(username):
    return requests.get(f"{API_URL}/eligible-courses/{username}")


def get_blocked_courses(username):
    return requests.get(f"{API_URL}/blocked-courses/{username}")


def check_schedule(selected_courses):
    return requests.post(
        f"{API_URL}/check-schedule",
        json={"selected_courses": selected_courses}
    )

def generate_curriculum_map(username):
    return requests.post(
        f"{API_URL}/curriculum-map",
        json={"username": username}
    )
