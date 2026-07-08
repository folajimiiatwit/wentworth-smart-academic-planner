"""
Calendar configuration utilities.

This file stores shared calendar settings and event-building helpers used by
the schedule page.

Main responsibilities:
- Define calendar display options
- Convert course data into calendar events
- Keep calendar configuration separate from page logic
"""
from datetime import datetime, timedelta

DAY_MAP = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
}

CALENDAR_OPTIONS = {
    "editable": False,
    "selectable": False,
    "headerToolbar": False,
    "slotMinTime": "08:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "timeGridWeek",
    "dayHeaderFormat": {"weekday": "long"},
    "allDaySlot": False,
    "contentHeight": 600,
    "height": 650,
    "expandRows": True,
    "firstDay": 1,
    "weekends": False,
}

def get_week_start():
    """
    Return the date for the Monday of the current week.

    Returns:
        datetime: Date and time representing the current week's Monday.
    """
    today = datetime.today()
    return today - timedelta(days=today.weekday())

def build_events(courses):
    """
    Convert course records into dated calendar events for the schedule page.

    Args:
        courses (list[dict]): Course records with title, days, start time, and end time.

    Returns:
        list[dict]: Calendar event dictionaries with start and end datetimes.
    """
    week_start = get_week_start()
    events = []
    for course in courses:
        for day in course["days"]:
            date = week_start + timedelta(days=DAY_MAP[day])
            events.append({
                "title": course["title"],
                "start": f"{date.strftime('%Y-%m-%d')}T{course['start_time']}",
                "end": f"{date.strftime('%Y-%m-%d')}T{course['end_time']}",
            })
    return events