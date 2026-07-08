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
    """
    Checks whether the FastAPI backend is running and starts it if needed.

    The function first sends a health-check request to the backend. If the
    backend does not respond successfully, it starts the backend using Uvicorn
    and repeatedly checks until the server becomes available.

    Returns:
        None
    """
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
    """
    Checks whether the backend API is currently available.

    Returns:
        bool: True if the backend health endpoint responds successfully,
        otherwise False.
    """
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def login_user(username):
    """
    Sends a login request for the specified user.

    Args:
        username (str): The username entered by the user.

    Returns:
        requests.Response: The response returned by the backend login endpoint.
    """
    return requests.post(
        f"{API_URL}/login",
        json={"username": username}
    )


def get_completed_info(username):
    """
    Retrieves saved completed-course information for a user.

    Args:
        username (str): The username whose completed-course data should be retrieved.

    Returns:
        requests.Response: The backend response containing completed-course information.
    """
    return requests.get(f"{API_URL}/completed-info/{username}")


def get_required_courses():
    """
    Retrieves the list of required courses from the backend.

    Returns:
        requests.Response: The backend response containing required course data.
    """
    return requests.get(f"{API_URL}/required-courses")


def upload_transcript(uploaded_file):
    """
    Uploads a transcript file to the backend for parsing.

    Args:
        uploaded_file: The transcript file uploaded through the frontend.

    Returns:
        requests.Response: The backend response containing extracted course information.
    """
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
    """
    Saves completed required courses and elective credit information for a user.

    Args:
        username (str): The username associated with the saved data.
        completed_required_courses (list): A list of completed required course codes.
        elective_data (dict): Elective credit information to include in the saved record.

    Returns:
        requests.Response: The backend response confirming the save operation.
    """
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
    """
    Saves custom completed courses for a user.

    Args:
        username (str): The username associated with the custom completed courses.
        custom_completed_courses (list): A list of custom completed course records.

    Returns:
        requests.Response: The backend response confirming the save operation.
    """
    return requests.post(
        f"{API_URL}/save-custom-completed",
        json={
            "username": username,
            "custom_completed_courses": custom_completed_courses
        }
    )


def get_progress(username):
    """
    Retrieves curriculum progress information for a user.

    Args:
        username (str): The username whose progress should be retrieved.

    Returns:
        requests.Response: The backend response containing progress information.
    """
    return requests.get(f"{API_URL}/progress/{username}")


def get_eligible_courses(username):
    """
    Retrieves courses the user is currently eligible to take.

    Args:
        username (str): The username used to determine course eligibility.

    Returns:
        requests.Response: The backend response containing eligible courses.
    """
    return requests.get(f"{API_URL}/eligible-courses/{username}")


def get_blocked_courses(username):
    """
    Retrieves courses that are currently blocked for a user.

    Args:
        username (str): The username used to determine blocked courses.

    Returns:
        requests.Response: The backend response containing blocked courses.
    """
    return requests.get(f"{API_URL}/blocked-courses/{username}")


def check_schedule(selected_courses):
    """
    Sends selected courses to the backend to check for schedule conflicts.

    Args:
        selected_courses (list): A list of selected course objects or identifiers.

    Returns:
        requests.Response: The backend response containing schedule conflict results.
    """
    return requests.post(
        f"{API_URL}/check-schedule",
        json={"selected_courses": selected_courses}
    )

def generate_curriculum_map(username):
    """
    Requests generation of a curriculum map for a user.

    Args:
        username (str): The username used to generate the curriculum map.

    Returns:
        requests.Response: The backend response containing the generated curriculum map.
    """
    return requests.post(
        f"{API_URL}/curriculum-map",
        json={"username": username}
    )
