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
    "height": 650,
    "expandRows": True,
    "firstDay": 1,
}

def get_week_start():
    today = datetime.today()
    return today - timedelta(days=today.weekday())

def build_events(courses):
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