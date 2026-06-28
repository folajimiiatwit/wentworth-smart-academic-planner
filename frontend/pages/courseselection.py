import streamlit as st
import ui as ui
ui.page_config()
ui.render_header()
from pathlib import Path


st.write("Hi this is where the meat and potatoes of the app will be ")

BASE_DIR = Path(__file__).resolve().parent.parent

ui.set_png_as_page_bg(BASE_DIR/ "assets/background.jpg") 

#* note to self add a view of the calendar and split it in half such that there's the ability to pick classes and stuff while watching in real time 
# page flow will be 

with st.container():
    if st.button("Calendar App"):
        st.switch_page("pages/schedule.py")