# will hold helper method(s) for creating calendar
import datetime
from streamlit_calendar import calendar


def course_days_to_calendar_days(days_text):
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
    value = str(time_text).strip().lower()

    for fmt in ["%H:%M", "%I:%M%p", "%I:%M %p"]:
        try:
            parsed = datetime.datetime.strptime(value, fmt)
            return parsed.strftime("%H:%M:%S")
        except ValueError:
            pass

    return None


def course_color(course_code):
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
    options = {
        "initialView": "timeGridWeek",
        "headerToolbar": {
            "left": "",
            "center": "title",
            "right": ""
        },
        "allDaySlot": False,
        "slotMinTime": "08:00:00",
        "slotMaxTime": "18:00:00",
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