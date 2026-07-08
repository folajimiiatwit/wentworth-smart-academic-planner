"""
Purpose:
This provides helper functions for displaying selected courses on a calendar.

Main responsibilities:
- Convert course meeting days into calendar days
- Normalize course start and end times
- Assign colors to course subjects
- Build calendar events from selected courses
- Render the Streamlit calendar view
"""
import datetime
from streamlit_calendar import calendar


def course_days_to_calendar_days(days_text):
    """
    Convert course meeting-day abbreviations into FullCalendar weekday numbers.

    Args:
        days_text (str): Meeting-day text such as `MWF` or `TR`.

    Returns:
        list[int]: FullCalendar weekday numbers for Monday through Friday.
    """
    days_text = str(days_text).upper().replace(" ", "")
    days = []

    if "M" in days_text:
        days.append(1)
    if "T" in days_text:
        days.append(2)
    if "W" in days_text:
        days.append(3)
    if "R" in days_text:
        days.append(4)
    if "F" in days_text:
        days.append(5)

    return days


def normalize_calendar_time(time_text):
    """
    Normalize a course meeting time for calendar display.

    Args:
        time_text (str): Time string in 24-hour or 12-hour format.

    Returns:
        str | None: Time formatted as `HH:MM:SS`, or None if parsing fails.
    """
    value = str(time_text).strip().lower()

    for fmt in ["%H:%M", "%I:%M%p", "%I:%M %p"]:
        try:
            parsed = datetime.datetime.strptime(value, fmt)
            return parsed.strftime("%H:%M:%S")
        except ValueError:
            pass

    return None


def course_color(course_code):
    """
    Choose a display color based on a course subject prefix.

    Args:
        course_code (str): Course code such as `COMP1000`.

    Returns:
        str: Hex color value for calendar display.
    """
    prefix = "".join(
        [char for char in str(course_code) if char.isalpha()]
    ).upper()

    colors = {
        "COMP": "#F6C85F",
        "MATH": "#6FDD8B",
        "ENGL": "#7DB7FF",
        "PHYS": "#FFB86B",
        "CHEM": "#76D7C4",
        "COMM": "#D8BFD8",
        "PHIL": "#C4A484",
        "MGMT": "#ADD8E6",
        "COOP": "#D3D3D3"
    }

    return colors.get(prefix, "#B0B0B0")


def build_calendar_events(schedule):
    """
    Build FullCalendar event dictionaries from selected course records.

    Args:
        schedule (list[dict]): Selected course records.

    Returns:
        list[dict]: Calendar event dictionaries.
    """
    events = []

    for course in schedule:
        start_time = normalize_calendar_time(course.get("start_time", ""))
        end_time = normalize_calendar_time(course.get("end_time", ""))

        if start_time is None or end_time is None:
            continue

        days = course_days_to_calendar_days(course.get("days", ""))

        if not days:
            continue

        code = str(course.get("course_code", ""))
        section = str(course.get("section", ""))

        events.append({
            "title": f"{code}-{section}",
            "daysOfWeek": days,
            "startTime": start_time,
            "endTime": end_time,
            "backgroundColor": course_color(code),
            "borderColor": course_color(code),
            "textColor": "#000000"
        })

    return events


def show_calendar(schedule):
    """
    Render the selected schedule in a Streamlit weekly calendar.

    Args:
        schedule (list[dict]): Selected course records to display.
    """
    options = {
        "initialView": "timeGridWeek",
        "headerToolbar": {
            "left": "",
            "center": "title",
            "right": ""
        },
        "allDaySlot": False,
        "slotMinTime": "08:00:00",
        "slotMaxTime": "23:00:00",
        "slotDuration": "00:30:00",
        "height": 650,
        "expandRows": True,
        "weekends": False,
        "hiddenDays": [0, 6]
    }

    calendar(
        events=build_calendar_events(schedule),
        options=options,
        key="schedule_calendar"
    )