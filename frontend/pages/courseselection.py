"""
Course Selection page.

This Streamlit page allows students to manage completed academic information
before building a schedule.

Main responsibilities:
- Upload and analyze transcripts
- Add completed courses manually
- Display completed required and custom courses
- Enter completed elective credits
- Save completed information to the backend
- Display degree progress
- Generate an AI curriculum map
"""
import streamlit as st
import ui as ui
import data as data
from pathlib import Path
from frontend.util.course_selection_helpers import (
    require_login,
    load_user_data,
    transcript_upload_section,
    manual_course_section,
    completed_courses_section,
    elective_section,
    save_section,
    progress_section,
    curriculum_map_section
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

data.ensure_backend_running()

ui.set_png_as_page_bg(BASE_DIR/ "assets/background.jpg") 
ui.page_config()
ui.render_header()
st.title("Course Selection")

if st.button("Return to Schedule Builder"):
    st.switch_page("pages/schedule.py")


elective_saved = load_user_data()

tab1, tab2, tab3, tab4 = st.tabs([
    "Transcript",
    "Completed Courses",
    "Progress",
    "AI Plan"
])

with tab1:
    st.subheader("Transcript Upload")
    #Way to upload files here
    transcript_upload_section() 

    st.divider()

    st.subheader("Add Course Manually")
    #Way to add courses manually here (preferable by typing course name (eg. COMP), course number, and title(optional))
    manual_course_section()

with tab2:
    #show result of transcript analysis 
    completed_courses_section()

    st.divider()
    #where to update credits for electives
    elective_data = elective_section(elective_saved)

    #save results
    save_section(elective_data)
with tab3:
    #see current progress
    progress_section()

with tab4:
    #button to generate curiculum map
    curriculum_map_section()

st.divider()

bottom_left, bottom_right = st.columns([4, 1])

#* note to self add a view of the calendar and split it in half such that there's the ability to pick classes and stuff while watching in real time 
# page flow will be 

#with st.container():
#   if st.button("Calendar App"):
#        st.switch_page("pages/schedule.py")