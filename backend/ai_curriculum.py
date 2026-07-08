"""
Purpose:
Generates an AI-assisted curriculum map for a student.

Main responsibilities:
- Build a prompt using completed courses and remaining requirements
- Send the prompt to the OpenAI API
- Return a semester-by-semester recommendation
- Avoid recommending courses when all requirements are complete
"""
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def build_curriculum_prompt(
    completed_required_courses,
    remaining_required_courses,
    elective_details,
    semester_courses,
):
    """
    Builds the prompt used to generate an AI-assisted curriculum map.

    The prompt includes the student's completed required courses, remaining
    required courses, elective progress, and available semester courses. It also
    gives the AI model rules for creating a semester-by-semester academic plan.

    Args:
        completed_required_courses (list): Required courses the student has already completed.
        remaining_required_courses (list): Required courses the student still needs to complete.
        elective_details (dict): Elective credit progress and remaining elective requirements.
        semester_courses (list): Courses available in upcoming semesters.

    Returns:
        str: A formatted prompt to send to the AI model.
    """
    
    return f"""
You are an academic planning assistant for a Computer Science student at Wentworth.

Create a semester-by-semester curriculum map to help the student graduate.

Use these rules:
1. Do not include courses already completed.
2. Prioritize remaining required major courses first.
3. Include elective categories still needed.
4. Keep most semesters between 12 and 16 credits.
5. Respect prerequisites as much as possible based on the provided remaining required courses.
6. If a course is not clearly available in a semester, still place it as a future recommendation but mark it as "verify availability".
7. Output a clear table-style plan.
8. Also include a short explanation of why this plan makes sense.

Completed required courses:
{completed_required_courses}

Remaining required courses:
{remaining_required_courses}

Elective progress and remaining credits:
{elective_details}

Available semester courses:
{semester_courses}

Return the answer in this format:

Curriculum Map:
Semester | Recommended Courses | Credits | Notes

Then include:
Summary:
- Estimated remaining credits
- Most important next courses
- Warnings or assumptions
"""


def generate_curriculum_map(
    completed_required_courses,
    remaining_required_courses,
    elective_details,
    semester_courses,
):
    """
    Generates an AI-assisted curriculum map for a student.

    This function builds a curriculum-planning prompt, sends it to the OpenAI
    chat completion API, and returns a semester-by-semester recommendation.
    If the AI request fails, it returns an error message instead of stopping
    the application.

    Args:
        completed_required_courses (list): Required courses the student has already completed.
        remaining_required_courses (list): Required courses the student still needs to complete.
        elective_details (dict): Elective credit progress and remaining elective requirements.
        semester_courses (list): Courses available in upcoming semesters.

    Returns:
        str: The generated curriculum map, or an error message if generation fails.
    """
    prompt = build_curriculum_prompt(
        completed_required_courses,
        remaining_required_courses,
        elective_details,
        semester_courses,
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful academic advisor. "
                        "Give practical, clear, degree-planning advice. "
                        "Do not claim official graduation approval."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI curriculum map could not be generated: {error}"