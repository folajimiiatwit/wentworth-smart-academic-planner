"""
Purpose:
Provides reusable UI sections for the Course Selection page.

Main responsibilities:
- Check that the user is logged in
- Load saved user course data
- Handle transcript upload
- Handle manual course entry
- Display completed courses
- Collect elective credits
- Save completed course information
- Display degree progress
- Display AI curriculum map results
"""
import streamlit as st
import data as data


def require_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = None

    if not st.session_state.logged_in or not st.session_state.username:
        st.warning("Please login first.")

        if st.button("Back to Login"):
            st.switch_page("login.py")

        st.stop()

    if not data.api_available():
        st.error("Backend is not running.")
        st.stop()


def load_user_data():
    saved = data.get_completed_info(st.session_state.username).json()

    if "completed_required_courses" not in st.session_state:
        st.session_state.completed_required_courses = saved.get(
            "completed_required_courses",
            []
        )

    if "custom_completed_courses" not in st.session_state:
        st.session_state.custom_completed_courses = saved.get(
            "custom_completed_courses",
            []
        )

    return saved.get("elective_credits", {})


def transcript_upload_section():
    st.subheader("Upload Transcript")

    uploaded_file = st.file_uploader(
        "Upload transcript",
        type=["pdf", "docx"]
    )

    if uploaded_file is not None and st.button("Analyze Transcript"):
        response = data.upload_transcript(uploaded_file)

        if response.status_code == 200:
            result = response.json()

            imported_required = result.get("completed_required_courses", [])
            imported_custom = result.get("custom_completed_courses", [])

            st.session_state.completed_required_courses = sorted(
                set(
                    st.session_state.completed_required_courses
                    + imported_required
                )
            )

            existing_custom = [
                course["course_code"]
                for course in st.session_state.custom_completed_courses
            ]

            for course in imported_custom:
                if course["course_code"] not in existing_custom:
                    st.session_state.custom_completed_courses.append(course)

            st.success("Transcript analyzed successfully.")
        else:
            st.error("Transcript could not be analyzed.")


def manual_course_section():

    with st.form("manual_course_form"):
        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            subject = st.text_input("Course Code", placeholder="COMP")

        with col2:
            number = st.text_input("Course Number", placeholder="1000")

        with col3:
            title = st.text_input(
                "Course Title",
                placeholder="Computer Science I"
            )

        add_course = st.form_submit_button("Add Course")

        if add_course:
            if subject.strip() == "" or number.strip() == "":
                st.error("Please enter both course code and course number.")
                return

            full_code = f"{subject.strip().upper()}{number.strip()}"

            required_response = data.get_required_courses()

            if required_response.status_code != 200:
                st.error("Could not load required courses.")
                return

            required_courses = required_response.json()
            required_codes = [
                course["course_code"]
                for course in required_courses
            ]

            if full_code in required_codes:
                if full_code not in st.session_state.completed_required_courses:
                    st.session_state.completed_required_courses.append(full_code)
                    st.success(f"Added {full_code} as a completed required course.")
                else:
                    st.warning(f"{full_code} is already listed.")
            else:
                existing_custom = [
                    course["course_code"]
                    for course in st.session_state.custom_completed_courses
                ]

                if full_code not in existing_custom:
                    st.session_state.custom_completed_courses.append({
                        "course_code": full_code,
                        "course_number": number.strip(),
                        "title": title.strip() or "Manually Added Course"
                    })
                    st.success(f"Added {full_code} as a custom completed course.")
                else:
                    st.warning(f"{full_code} is already listed.")


def completed_courses_section():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Completed Required Courses")

        if st.session_state.completed_required_courses:
            st.dataframe(
                [{"Course Code": course} for course in st.session_state.completed_required_courses],
                width="stretch",
                height=350
            )
        else:
            st.info("No completed required courses yet.")

    with col2:
        st.subheader("Other Completed Courses")

        if st.session_state.custom_completed_courses:
            st.dataframe(
                st.session_state.custom_completed_courses,
                width="stretch",
                height=350
            )

            remove_options = [
                course["course_code"]
                for course in st.session_state.custom_completed_courses
            ]

            courses_to_remove = st.multiselect(
                "Remove custom completed courses",
                remove_options
            )

            if st.button("Remove Selected Custom Courses"):
                st.session_state.custom_completed_courses = [
                    course
                    for course in st.session_state.custom_completed_courses
                    if course["course_code"] not in courses_to_remove
                ]

                st.success("Selected courses removed.")
        else:
            st.info("No custom completed courses yet.")


def elective_section(elective_saved):
    st.subheader("Completed Elective Credits")

    col1, col2 = st.columns(2)

    values = {}

    with col1:
        values["general_elective_credits"] = st.number_input(
            "General Elective Credits / 8",
            0,
            100,
            int(elective_saved.get("general_elective_credits", 0))
        )

        values["cs_elective_credits"] = st.number_input(
            "Computer Science Elective Credits / 16",
            0,
            100,
            int(elective_saved.get("cs_elective_credits", 0))
        )

        values["english_elective_credits"] = st.number_input(
            "English Elective Credits / 8",
            0,
            100,
            int(elective_saved.get("english_elective_credits", 0))
        )

        values["science_elective_credits"] = st.number_input(
            "Science Elective Credits / 8",
            0,
            100,
            int(elective_saved.get("science_elective_credits", 0))
        )

    with col2:
        values["humanities_elective_credits"] = st.number_input(
            "Humanities Elective Credits / 4",
            0,
            100,
            int(elective_saved.get("humanities_elective_credits", 0))
        )

        values["social_science_elective_credits"] = st.number_input(
            "Social Science Elective Credits / 4",
            0,
            100,
            int(elective_saved.get("social_science_elective_credits", 0))
        )

        values["ethics_elective_credits"] = st.number_input(
            "Ethics Elective Credits / 4",
            0,
            100,
            int(elective_saved.get("ethics_elective_credits", 0))
        )

    return values


def save_section(elective_data):
    if st.button("Save Completed Information"):
        completed_response = data.save_completed_info(
            st.session_state.username,
            st.session_state.completed_required_courses,
            elective_data
        )

        custom_response = data.save_custom_completed(
            st.session_state.username,
            st.session_state.custom_completed_courses
        )

        if completed_response.status_code == 200 and custom_response.status_code == 200:
            st.success("Completed course information saved.")
        else:
            st.error("Could not save completed information.")
            st.write("Completed info status:", completed_response.status_code)
            st.write("Custom courses status:", custom_response.status_code)


def progress_section():
    st.subheader("Progress")
    
    response = data.get_progress(st.session_state.username)

    if response.status_code != 200:
        st.error("Could not load progress.")
        return

    progress = response.json()

    remaining_required = (
        progress["total_required_credits"]
        - progress["completed_required_credits"]
    )

    col1, col2 = st.columns(2)

    col1.metric("Required Course Credits Remaining", remaining_required)
    col2.metric("Required Course Progress", f'{progress["required_percent"]}%')

    st.progress(progress["required_percent"] / 100)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Elective Credits Remaining")
        st.dataframe(progress["elective_details"], width="stretch")
    with col4:
        st.subheader("Remaining Required Courses")
        st.dataframe(progress["remaining_required_courses"], width="stretch")


def curriculum_map_section():
    st.subheader("AI Curriculum Map")

    if "curriculum_map_result" not in st.session_state:
        st.session_state.curriculum_map_result = ""

    if st.button("Generate AI Curriculum Map"):
        with st.spinner("Generating curriculum map..."):
            response = data.generate_curriculum_map(st.session_state.username)

        if response.status_code == 200:
            result = response.json()
            st.session_state.curriculum_map_result = result.get(
                "curriculum_map",
                ""
            )
        else:
            st.error("Could not generate curriculum map.")

    if st.session_state.curriculum_map_result:
        st.markdown(st.session_state.curriculum_map_result)