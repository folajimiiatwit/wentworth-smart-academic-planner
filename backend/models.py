"""
Pydantic request models for backend API endpoints.

This file defines the expected structure of request bodies sent from the
frontend to the FastAPI backend.

Main responsibilities:
- Validate login requests
- Validate completed course submissions
- Validate custom completed courses
- Validate schedule-check requests
- Validate AI curriculum-map requests
"""
from pydantic import BaseModel
from typing import List


class LoginRequest(BaseModel):
    username: str


class CompletedCoursesRequest(BaseModel):
    username: str
    completed_required_courses: List[str]
    general_elective_credits: int
    cs_elective_credits: int
    english_elective_credits: int
    science_elective_credits: int
    humanities_elective_credits: int
    social_science_elective_credits: int
    ethics_elective_credits: int


class ScheduleCheckRequest(BaseModel):
    selected_courses: List[str]


class CustomCompletedCourse(BaseModel):
    course_code: str
    course_number: str
    title: str


class CustomCompletedCoursesRequest(BaseModel):
    username: str
    custom_completed_courses: List[CustomCompletedCourse]

class CurriculumMapRequest(BaseModel):
    username: str

class TranscriptSaveRequest(BaseModel):
    username: str
    completed_required_courses: List[str]
    custom_completed_courses: List[CustomCompletedCourse]

