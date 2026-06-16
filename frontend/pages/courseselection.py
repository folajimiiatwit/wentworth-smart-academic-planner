import streamlit as st

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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-style">
    <h1>Wentworth Smart Academic Planner</h1>
    <p>TESTING Version 0.001</p>
</div>
""", unsafe_allow_html=True)
st.set_page_config(page_title='Wentworth Smart Academic Planner', layout="wide")

st.write("Hi this is where the meat and potatoes of the app will be ")

#* note to self add a view of the calendar and split it in half such that there's the ability to pick classes and stuff while watching in real time 
# page flow will be 

with st.container():
    if st.button("Calendar App"):
        st.switch_page("pages/main.py")
    if st.button("Course Selection"):
        st.switch_page("pages/courseselection.py")