"""
Shared Streamlit UI utilities.

This file contains reusable styling and layout functions used across the
frontend pages.

Main responsibilities:
- Configure Streamlit page settings
- Render the shared application header
- Set a background image
- Keep styling code separate from page logic
"""
import streamlit as st
import sys
import os
from pathlib import Path
import base64
 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def page_config(title="Wentworth Smart Academic Planner"):
    """
    Apply shared Streamlit page settings for the application.

    Args:
        title (str): Browser page title to display for the Streamlit app.
    """
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
    """
    Render the shared application title and version header.
    """
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
        <p>TESTING Version 0.5</p>
    </div>
    """, unsafe_allow_html=True)


def set_background(image_file: str):
    """
    Set a background image for the current Streamlit page.

    Args:
        image_file (str): Path to the image file to use as the background.
    """
    image_path = Path(image_file)

    with open(image_path, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background-image:
                    linear-gradient(rgba(20, 20, 40, 0.35), rgba(20, 20, 40, 0.35)),
                    url("data:image/jpg;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            .main {{
                background: transparent;
            }}

            [data-testid="stMainBlockContainer"] {{
                background: transparent;
                box-shadow: none;
            }}

            .header-style {{
                background: linear-gradient(135deg, #6a00fc 0%, #ffa10c 80%);
                padding: 10px 20px;
                border-radius: 8px;
                color: white;
                margin-bottom: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}

            [data-testid="collapsedControl"] {{
                display: none;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    """
    Read a binary file and return its Base64-encoded string.

    Args:
        bin_file (str | pathlib.Path): Path to the binary file.

    Returns:
        str: Base64-encoded file content.
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    """
    Set a PNG image as the Streamlit page background.

    Args:
        png_file (str | pathlib.Path): Path to the PNG background image.
    """
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return