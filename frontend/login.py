import streamlit as st
import ui as ui
from backend.auth import login_user
ui.page_config()
ui.render_header()

with st.sidebar:
    st.sidebar.write()

# wrap this in a simple true false if a new user or login found

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username").strip().lower()

    if st.button("Login"):
        if username:
            result = login_user(username)
            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
        else:
            st.warning("Please enter a username.")
else:
    st.switch_page("pages/schedule.py")

# backup in case more pages are necessary
# if st.button("Page 2"):
    # st.switch_page("pages/page_2.py")

