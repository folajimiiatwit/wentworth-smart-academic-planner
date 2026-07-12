"""
Login page.

This Streamlit page is the entry point of the application.

Main responsibilities:
- Display the username login form
- Check backend availability
- Send login requests to the backend
- Store login status and username in Streamlit session state
- Redirect logged-in users to the schedule page
"""
import streamlit as st
import ui as ui
import data as data
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

data.ensure_backend_running()
ui.set_png_as_page_bg(BASE_DIR/ "assets/background.jpg") 

left, center, right = st.columns([2, 1.5, 2])

with center:
    
    ui.page_config()
    ui.render_header()

    with st.sidebar:
        st.sidebar.write()

    # wrap this in a simple true false if a new user or login found

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    if not data.api_available():
        st.error("Backend is not running.")
        st.stop()

    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username").strip().lower()

        if st.button("Login"):
            if username:
                result = data.login_user(username)
                if result.status_code != 200:
                    st.error("Login Failed.")
                else:
                    result = result.json()

                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.session_state.logged_in = True
                        st.session_state.username = result["username"]
                        st.rerun()
            else:
                st.warning("Please enter a username.")
    else:
        st.switch_page("pages/schedule.py")
