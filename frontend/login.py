import streamlit as st
st.set_page_config(page_title='Wentworth Smart Academic Planner', layout="wide", initial_sidebar_state="collapsed")

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
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-style">
    <h1>Wentworth Smart Academic Planner</h1>
    <p>TESTING Version 0.001</p>
</div>
""", unsafe_allow_html=True)



st.write("Hi this is where the login would be, the buttons below will only appear after a user is logged in or whatnot")

# wrap this in a simple true false if a new user or login found
with st.container():
    if st.button("Calendar App"):
        st.switch_page("pages/main.py")
    if st.button("Course Selection"):
        st.switch_page("pages/courseselection.py")


# backup in case more pages are necessary
# if st.button("Page 2"):
    # st.switch_page("pages/page_2.py")

