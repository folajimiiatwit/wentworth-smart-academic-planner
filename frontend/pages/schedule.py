import streamlit as st
from streamlit_calendar import calendar
import ui as ui
from util.config import build_events, CALENDAR_OPTIONS

ui.page_config()
ui.render_header()

col_courses, col_calendar = st.columns([1, 3])

if "selected_courses" not in st.session_state:
    st.session_state.selected_courses = []

courses = [
    {
        "title": "Example Class",
        "days": ["Monday", "Wednesday"],
        "start_time": "08:00:00",
        "end_time": "09:30:00",
    },
    {
        "title": "Example Class (Lab)",
        "days": ["Thursday"],
        "start_time": "10:40:00",
        "end_time": "12:30:00",
    },
]

col_courses, col_calendar = st.columns([1, 3])

with col_courses:
    st.subheader("Your Courses")
    if not courses:
        st.info("Course list will appear here")
    else:
        for course in courses:
            with st.container(border=True):
                st.write(f"**{course['title']}**")
                st.caption(f"{', '.join(course['days'])} • {course['start_time'][:-3]} - {course['end_time'][:-3]}")

with col_calendar:
    custom_css = """
    .fc-event-time { font-style: italic; }
    .fc-event-title { font-weight: 700; }
    .fc-event { background-color: #6a00fc; border-color: #6a00fc; }
    """

    cal_result = calendar(
        events=build_events(courses),
        options=CALENDAR_OPTIONS,
        custom_css=custom_css,
        key='calendar',
    )
    