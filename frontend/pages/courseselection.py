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

#* note to self add a view of the calendar and split it in half such that there's the ability to pick classes and stuff while watching in real time 
# page flow will be 

with st.container():
    if st.button("Calendar App"):
        st.switch_page("pages/schedule.py")