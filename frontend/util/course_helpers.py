"""
Purpose:
Provides helper functions for formatting and organizing course data.

Main responsibilities:
- Group courses by subject or category
- Create unique course section identifiers
- Format course labels for display in the schedule builder
"""
def group_courses(courses):
    grouped = {}

    for course in courses:
        group = course.get("group", "OTHER")

        if group not in grouped:
            grouped[group] = []

        grouped[group].append(course)

    return dict(sorted(grouped.items()))


def section_id(course):
    if "crn" in course and str(course["crn"]).strip() != "":
        return str(course["crn"])

    return f'{course["course_code"]}-{course["section"]}'


def section_label(course):
    return (
        f'{course["course_code"]}-{course["section"]} '
        f'CRN {course.get("crn", "")}: '
        f'{course["title"]} '
        f'({course["days"]} {course["start_time"]}-{course["end_time"]})'
    )