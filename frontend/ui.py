import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def page_config(title="Wentworth Smart Academic Planner"):
    st.set_page_config(
        page_title=title,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.markdown("""
    <style>
        [data-testid="collapsedControl"] { display: none }
        section[data-testid="stSidebar"] { display: none }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <style>
        [data-testid="collapsedControl"] { display: none }
        .header-style {
            background: linear-gradient(135deg, #6a00fc 0%, #ffa10c 80%);
            padding: 10px;
            border-radius: 5px;
            color: white;
            margin-bottom: 10px;
        }
    </style>
    <div class="header-style">
        <h1>Wentworth Smart Academic Planner</h1>
        <p>TESTING Version 0.010</p>
    </div>
    """, unsafe_allow_html=True)