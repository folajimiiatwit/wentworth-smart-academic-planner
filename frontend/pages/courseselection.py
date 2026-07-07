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

st.write("Hi this is where the meat and potatoes of the app will be ")

BASE_DIR = Path(__file__).resolve().parent.parent.parent

data.ensure_backend_running()

ui.set_png_as_page_bg(BASE_DIR/ "assets/background.jpg") 
ui.page_config()
ui.render_header()
st.title("Course Selection")
st.caption("Manage completed courses, elective credits, and degree progress.")


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

#move to calandar page
with bottom_right:
    if st.button("Schedule Builder", width="stretch"):
        st.switch_page("pages/schedule.py")
#* note to self add a view of the calendar and split it in half such that there's the ability to pick classes and stuff while watching in real time 
# page flow will be 

#with st.container():
#   if st.button("Calendar App"):
#        st.switch_page("pages/schedule.py")