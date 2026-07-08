"""
Purpose:
Provides helper functions for formatting and organizing course data.

Main responsibilities:
- Group courses by subject or category
- Create unique course section identifiers
- Format course labels for display in the schedule builder
"""
def group_courses(courses):
    """
    Group course records by their subject or category group.

    Args:
        courses (list[dict]): Course records to group.

    Returns:
        dict: Course records grouped by subject/category.
    """
    grouped = {}

    for course in courses:
        group = course.get("group", "OTHER")

        if group not in grouped:
            grouped[group] = []

        grouped[group].append(course)

    return dict(sorted(grouped.items()))


def section_id(course):
    """
    Return a unique identifier for a course section.

    The CRN is used when available; otherwise the function falls back to
    `course_code-section`.

    Args:
        course (dict): Course section record.

    Returns:
        str: Unique section identifier.
    """
    if "crn" in course and str(course["crn"]).strip() != "":
        return str(course["crn"])

    return f'{course["course_code"]}-{course["section"]}'


def section_label(course):
    """
    Build a human-readable label for a course section.

    Args:
        course (dict): Course section record.

    Returns:
        str: Display label containing code, section, CRN, title, days, and times.
    """
    return (
        f'{course["course_code"]}-{course["section"]} '
        f'CRN {course.get("crn", "")}: '
        f'{course["title"]} '
        f'({course["days"]} {course["start_time"]}-{course["end_time"]})'
    )