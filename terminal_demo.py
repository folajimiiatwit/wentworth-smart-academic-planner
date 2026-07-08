
"""
Purpose:
Provides a terminal-based demo version of the Wentworth Smart Academic Planner. (ONLY used during 1st presentation and has no significance to final product)

Main responsibilities:
- Allow users to log in from the terminal
- Display required, eligible, and blocked courses
- Save completed course and elective information
- Check selected schedules for conflicts
- Show degree-progress information without using the Streamlit frontend
"""
from backend.auth import login_user
from backend.data_manager import (
    load_required_courses,
    load_semester_courses,
    get_completed_required_courses,
    get_elective_credits,
    save_completed_info
)
from backend.planner import (
    get_eligible_semester_courses,
    get_blocked_semester_courses,
    required_progress,
    check_schedule
)


def print_header(title):
    """
    Prints a formatted section header in the terminal.

    Args:
        title (str): Header text to display.

    Returns:
        None
    """
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)


def required_input(prompt):
    """
    Repeatedly prompts the user until a non-empty value is entered.

    Args:
        prompt (str): Text shown to the user.

    Returns:
        str: The non-empty user input.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def int_input(prompt, minimum=0, maximum=100, allow_blank=False, current=0):
    """
    Prompts the user for an integer within a valid range.

    Args:
        prompt (str): Text shown to the user.
        minimum (int): Lowest allowed value.
        maximum (int): Highest allowed value.
        allow_blank (bool): Whether the user may leave the input blank.
        current (int): Value returned when blank input is allowed.

    Returns:
        int: The validated integer entered by the user.
    """
    while True:
        value = input(prompt).strip()

        if allow_blank and value == "":
            return current

        try:
            number = int(value)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if number < minimum or number > maximum:
            print(f"Enter a number from {minimum} to {maximum}.")
            continue

        return number


def parse_codes(text):
    """
    Converts comma-separated course codes into a cleaned list.

    Args:
        text (str): Comma-separated course-code text.

    Returns:
        list[str]: Uppercase course codes with extra spaces removed.
    """
    return [item.strip().upper() for item in text.split(",") if item.strip()]


def get_custom_codes(username):
    """
    Retrieves custom completed course codes for a user.

    Args:
        username (str): Username whose custom courses should be retrieved.

    Returns:
        list[str]: Custom completed course codes, or an empty list if retrieval fails.
    """
    try:
        from backend.data_manager import get_custom_completed_courses
        return [course["course_code"] for course in get_custom_completed_courses(username)]
    except Exception:
        return []


def get_all_completed_codes(username):
    """
    Combines required and custom completed course codes for a user.

    Args:
        username (str): Username whose completed courses should be retrieved.

    Returns:
        list[str]: All completed course codes for the user.
    """
    return get_completed_required_courses(username) + get_custom_codes(username)


def save_custom_course(username, code, number, title):
    """
    Saves a custom completed course for a user if it does not already exist.

    Args:
        username (str): Username associated with the custom course.
        code (str): Full course code.
        number (str): Course number.
        title (str): Course title.

    Returns:
        bool: True if the course is saved successfully, otherwise False.
    """
    try:
        from backend.data_manager import get_custom_completed_courses, save_custom_completed_courses
        custom = get_custom_completed_courses(username)
        existing = [course["course_code"] for course in custom]

        if code not in existing:
            custom.append({
                "course_code": code,
                "course_number": number,
                "title": title
            })

        save_custom_completed_courses(username, custom)
        return True
    except Exception:
        return False


def show_courses(courses, limit=50):
    """
    Displays course records in the terminal.

    Args:
        courses (list[dict]): Course records to display.
        limit (int): Maximum number of courses to show.

    Returns:
        None
    """
    if not courses:
        print("No courses found.")
        return

    for i, course in enumerate(courses[:limit], 1):
        code = course.get("course_code", "")
        section = course.get("section", "")
        crn = course.get("crn", "")
        title = course.get("title", "")
        days = course.get("days", "")
        start = course.get("start_time", "")
        end = course.get("end_time", "")
        prereq = course.get("prerequisites", "")

        label = f"{code}-{section}" if section else code
        print(f"{i}. {label} | CRN: {crn} | {title}")
        if days or start or end:
            print(f"   Time: {days} {start}-{end}")
        print(f"   Prerequisites: {prereq if prereq else 'None'}")


def save_required_courses(username):
    print_header("Save Completed Required Courses")
    required_df = load_required_courses()
    valid_codes = set(required_df["course_code"].astype(str).str.upper())

    print("Enter required course codes separated by commas.")
    print("Example: COMP1000,COMP1050,MATH2300")
    print("Leave blank to clear saved required courses.")

    while True:
        text = input("Completed required courses: ").strip()
        codes = parse_codes(text)

        invalid = [code for code in codes if code not in valid_codes]
        if invalid:
            print("Invalid required course code(s): " + ", ".join(invalid))
            print("Use option 3 for custom/transfer courses.")
            continue

        save_completed_info(username, codes, get_elective_credits(username))
        print("Completed required courses saved.")
        return


def add_custom_course(username):
    print_header("Add Custom Completed Course")

    prefix = required_input("Course prefix, e.g., MATH: ").upper()
    while not prefix.isalpha():
        print("Prefix should contain letters only.")
        prefix = required_input("Course prefix, e.g., MATH: ").upper()

    number = required_input("Course number, e.g., 2800: ")
    while not number.isdigit():
        print("Course number should contain digits only.")
        number = required_input("Course number, e.g., 2800: ")

    title = input("Course title, optional: ").strip() or "Custom Completed Course"
    code = f"{prefix}{number}"

    if save_custom_course(username, code, number, title):
        print(f"Saved custom completed course: {code}")
    else:
        print("Custom course saving is not supported in this backend version.")


def enter_electives(username):
    print_header("Enter Elective Credits")
    data = get_elective_credits(username)

    fields = [
        ("general_elective_credits", "General Elective Credits / 8"),
        ("cs_elective_credits", "Computer Science Elective Credits / 16"),
        ("english_elective_credits", "English Elective Credits / 8"),
        ("science_elective_credits", "Science Elective Credits / 8"),
        ("humanities_elective_credits", "Humanities Elective Credits / 4"),
        ("social_science_elective_credits", "Social Science Elective Credits / 4"),
        ("ethics_elective_credits", "Ethics Elective Credits / 4")
    ]

    print("Press Enter to keep current value.")

    for key, label in fields:
        current = data.get(key, 0)
        data[key] = int_input(f"{label} current={current}: ", allow_blank=True, current=current)

    save_completed_info(username, get_completed_required_courses(username), data)
    print("Elective credits saved.")


def view_progress(username):
    print_header("Progress")
    progress = required_progress(
        load_required_courses(),
        get_completed_required_courses(username),
        get_elective_credits(username)
    )

    print(f"Completed required credits: {progress['completed_required_credits']}")
    print(f"Completed elective credits: {progress['completed_elective_credits']}")
    print(f"Total completed credits: {progress['total_completed_credits']}")
    print(f"Overall progress: {progress['total_percent']}%")

    print("\nElective progress:")
    for item in progress["elective_details"]:
        print(f"- {item['category']}: {item['completed']}/{item['required']} credits")


def view_eligible(username):
    print_header("Eligible Semester Courses")
    eligible = get_eligible_semester_courses(load_semester_courses(), get_all_completed_codes(username))
    show_courses(eligible.to_dict(orient="records"), limit=100)


def view_blocked(username):
    print_header("Blocked Courses")
    blocked = get_blocked_semester_courses(load_semester_courses(), get_all_completed_codes(username))

    if not blocked:
        print("No blocked courses.")
        return

    for course in blocked:
        print(f"- {course.get('course_code')}: {course.get('title')}")
        print(f"  Reason: {course.get('reason')}")


def build_schedule(username):
    print_header("Build and Check Schedule")
    semester_df = load_semester_courses()
    eligible_df = get_eligible_semester_courses(semester_df, get_all_completed_codes(username))
    eligible = eligible_df.to_dict(orient="records")

    if not eligible:
        print("No eligible courses available.")
        return

    valid_crns = set()
    print("Eligible courses:")
    for course in eligible:
        crn = str(course.get("crn", "")).strip()
        valid_crns.add(crn)
        print(f"CRN {crn}: {course.get('course_code')}-{course.get('section')} | {course.get('title')} | {course.get('days')} {course.get('start_time')}-{course.get('end_time')}")

    while True:
        text = input("Enter CRNs to add, separated by commas: ").strip()
        if text == "":
            print("No CRNs entered. Returning to menu.")
            return

        crns = [item.strip() for item in text.split(",") if item.strip()]
        invalid = [crn for crn in crns if crn not in valid_crns]

        if invalid:
            print("Invalid or ineligible CRN(s): " + ", ".join(invalid))
            continue

        break

    result = check_schedule(semester_df, crns)

    print("\nSelected schedule:")
    for course in result["schedule"]:
        print(f"- {course.get('course_code')}-{course.get('section')} | {course.get('title')} | {course.get('days')} {course.get('start_time')}-{course.get('end_time')}")

    print(f"\nTotal credits: {result['total_credits']}")

    if result["conflicts"]:
        print("\nSchedule conflicts found:")
        for conflict in result["conflicts"]:
            print(f"- {conflict['course_1']} conflicts with {conflict['course_2']}")
    else:
        print("\nNo schedule conflicts found.")


def main():
    print_header("Wentworth Smart Planner - Demo")
    username = required_input("Enter username: ").lower()

    result = login_user(username)
    if "error" in result:
        print(result["error"])
        return

    print(f"Logged in as: {username}")

    actions = {
        "1": lambda: show_courses(load_required_courses().to_dict(orient="records"), limit=100),
        "2": lambda: save_required_courses(username),
        "3": lambda: add_custom_course(username),
        "4": lambda: enter_electives(username),
        "5": lambda: view_progress(username),
        "6": lambda: view_eligible(username),
        "7": lambda: view_blocked(username),
        "8": lambda: build_schedule(username)
    }

    while True:
        print_header("Menu")
        print("1. View required courses")
        print("2. Save completed required courses")
        print("3. Add custom completed course")
        print("4. Enter elective credits")
        print("5. View progress")
        print("6. View eligible semester courses")
        print("7. View blocked courses")
        print("8. Build/check schedule")
        print("9. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "9":
            print("Goodbye.")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid option. Enter a number from 1 to 9.")
            continue

        try:
            action()
        except Exception as error:
            print("An unexpected error occurred.")
            print(f"Error details: {error}")


if __name__ == "__main__":
    main()
