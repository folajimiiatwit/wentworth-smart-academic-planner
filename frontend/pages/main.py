import streamlit as st
import pandas as pd
import numpy as np
from streamlit_calendar import calendar

st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main {
        background-color: #f8f9fa;
    }
    .header-style {
        background: linear-gradient(135deg, #6a00fc 0%, #ffa10c 80%);
        padding: 10px;
        border-radius: 5px;
        color: white;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-style">
    <h1>Wentworth Smart Academic Planner</h1>
    <p>TESTING Version 0.001</p>
</div>
""", unsafe_allow_html=True)
st.set_page_config(page_title='Wentworth Smart Academic Planner', layout="wide")

with st.container():
    if st.button("Calendar App"):
        st.switch_page("pages/main.py")
    if st.button("Course Selection"):
        st.switch_page("pages/courseselection.py")


calendar_options = {
    "editable": False,
    "selectable": False,
    "headerToolbar": {
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "allDay" : "false",

    "initialView": "dayGridWeek",
    "headerToolbar" : "false",
    "resourceGroupField": "building",
    "resources": [],
}
calendar_events = [
    {
        "title": "Example Class",
        "start": "2026-06-15T08:00:00",
        "end": "2026-06-15T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Example Class",
        "start": "2026-06-17T08:00:00",
        "end": "2023-06-17T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Example Class (Lab)",
        "start": "2026-06-18T10:40:00",
        "end": "2026-06-18T12:30:00",
        "resourceId": "a",
    }
]
custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

calendar = calendar(
    events=calendar_events,
    options=calendar_options,
    custom_css=custom_css,
    key='calendar', # Assign a widget key to prevent state loss
    )
st.write(calendar)
