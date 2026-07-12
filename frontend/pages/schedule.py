"""
Schedule Builder page.

This Streamlit page allows students to select eligible course sections and
view their schedule in a calendar layout.

Main responsibilities:
- Load eligible courses from the backend
- Load blocked courses when prerequisites are not met
- Allow students to select course sections
- Check selected courses for time conflicts
- Display selected courses in a calendar view
"""
import streamlit as st
from streamlit_calendar import calendar
import ui as ui
from util.config import build_events, CALENDAR_OPTIONS
from pathlib import Path
import data as data
from frontend.util.course_helpers import group_courses, section_id, section_label
from frontend.util.calendar_helpers import show_calendar
from frontend.util.course_selection_helpers import require_login

BASE_DIR = Path(__file__).resolve().parent.parent.parent

data.ensure_backend_running()
ui.set_png_as_page_bg(BASE_DIR/ "assets/background.jpg")
ui.page_config()
ui.render_header()

require_login()

st.title("Schedule Builder")

if st.button("Course Selection"):
    st.switch_page("pages/courseselection.py")

eligible_response = data.get_eligible_courses(st.session_state.username)
blocked_response = data.get_blocked_courses(st.session_state.username)

if eligible_response.status_code != 200 or blocked_response.status_code != 200:
    st.error("Could not load schedule data.")
    st.stop()

eligible_courses = eligible_response.json()
blocked_courses = blocked_response.json()
selected = []

col_courses, col_calendar = st.columns([1.5, 4])

with col_courses:
    st.subheader("Eligible Courses")
    for group_name, group_items in group_courses(eligible_courses).items():
      with st.expander(group_name, expanded=True):
            ids = [section_id(course) for course in group_items]
            labels = {section_id(course): section_label(course) for course in group_items}

            selected.extend(
                st.multiselect(
                    f"Add {group_name} courses",
                    ids,
                    format_func=lambda code, labels=labels: labels.get(code, code),
                    key=f"select_{group_name}"
                )
            )
    
    st.subheader("Blocked Courses")
    for group_name, group_items in group_courses(blocked_courses).items():
        with st.expander(group_name, expanded=False):
            st.dataframe(group_items, width="stretch")  

with col_calendar:
    st.subheader("Selected Schedule")
    if not selected:
        st.info("Select eligible courses from the left.")
    
    else:
        result_response = data.check_schedule(selected)
        if result_response.status_code == 200:
            result = result_response.json()
            st.write(f'Total credits: **{result["total_credits"]}**')
            if result["conflicts"]:
                st.error("Schedule conflicts found.")
                st.dataframe(result["conflicts"], width="stretch")
            if st.radio("View schedule as", ["Calendar View", "Table View"], horizontal=True) == "Calendar View":
                show_calendar(result["schedule"])
            else:
                st.dataframe(result["schedule"], width="stretch")   
    