"""
Purpose:
Contains academic planning and schedule logic.

Main responsibilities:
- Evaluate prerequisite requirements
- Determine eligible courses
- Determine blocked courses
- Check selected courses for time conflicts
- Calculate degree progress and remaining requirements
"""
from datetime import datetime
import re

ELECTIVE_REQUIREMENTS = {
    "general_elective_credits": 8,
    "cs_elective_credits": 16,
    "english_elective_credits": 8,
    "science_elective_credits": 8,
    "humanities_elective_credits": 4,
    "social_science_elective_credits": 4,
    "ethics_elective_credits": 4
}


def get_course_group(course_code):
    """
    Extract the subject prefix from a course code.

    Examples include `COMP` from `COMP1000` and `MATH` from `MATH2300`.

    Args:
        course_code (str): Full course code.

    Returns:
        str: Uppercase subject group, or `OTHER` when no subject prefix is found.
    """
    match = re.match(r"([A-Za-z]+)", str(course_code).strip())
    if match:
        return match.group(1).upper()
    return "OTHER"


def add_course_groups(df):
    """
    Add a subject group column to a course DataFrame.

    Args:
        df (pandas.DataFrame): Course data containing a `course_code` column.

    Returns:
        pandas.DataFrame: Copy of the input DataFrame with an added `group` column.
    """
    df = df.copy()
    df["group"] = df["course_code"].apply(get_course_group)
    return df


def clean_course_code(course_code):
    """
    Normalize a course code by converting it to text and trimming whitespace.

    Args:
        course_code (str): Course code to clean.

    Returns:
        str: Cleaned course code.
    """
    return str(course_code).strip()


def tokenize_prerequisite_rule(rule):
    """
    Split a prerequisite expression into course-code and operator tokens.

    Supported operators are `&` for AND, `|` for OR, and parentheses for grouping.

    Args:
        rule (str): Prerequisite expression such as `COMP1050&(MATH2300|MATH2800)`.

    Returns:
        list[str]: Ordered prerequisite tokens.
    """
    rule = str(rule).replace(" ", "").strip()
    tokens = []
    current = ""

    for char in rule:
        if char.isalnum():
            current += char
        else:
            if current:
                tokens.append(current)
                current = ""
            if char in ["&", "|", "(", ")"]:
                tokens.append(char)

    if current:
        tokens.append(current)

    return tokens


def evaluate_prerequisite_rule(prerequisite_text, completed_courses):
    """
    Evaluates prerequisite rules with &, |, and parentheses.

    Examples:
    COMP1000
    COMP1000|ELEC3150
    COMP1000&MATH2300
    COMP1050&(MATH2300|MATH2800)
    """
    prerequisite_text = str(prerequisite_text).strip()

    if prerequisite_text == "" or prerequisite_text.lower() == "nan":
        return True

    completed_set = set(clean_course_code(course) for course in completed_courses)
    tokens = tokenize_prerequisite_rule(prerequisite_text)
    position = 0

    def parse_expression():
        nonlocal position
        value = parse_term()

        while position < len(tokens) and tokens[position] == "|":
            position += 1
            value = value or parse_term()

        return value

    def parse_term():
        nonlocal position
        value = parse_factor()

        while position < len(tokens) and tokens[position] == "&":
            position += 1
            value = value and parse_factor()

        return value

    def parse_factor():
        nonlocal position

        if position >= len(tokens):
            return False

        token = tokens[position]

        if token == "(":
            position += 1
            value = parse_expression()

            if position < len(tokens) and tokens[position] == ")":
                position += 1

            return value

        position += 1
        return clean_course_code(token) in completed_set

    try:
        return parse_expression()
    except Exception:
        return False


def missing_prerequisites(prerequisite_text, completed_courses):
    """
    Return a human-readable prerequisite warning when requirements are not met.

    Args:
        prerequisite_text (str): Prerequisite rule from the course data.
        completed_courses (list[str]): Course codes already completed by the student.

    Returns:
        str: Empty string when prerequisites are met, otherwise an explanation.
    """
    prerequisite_text = str(prerequisite_text).strip()

    if prerequisite_text == "" or prerequisite_text.lower() == "nan":
        return ""

    if evaluate_prerequisite_rule(prerequisite_text, completed_courses):
        return ""

    return "Prerequisite not met: " + prerequisite_text


def get_eligible_semester_courses(semester_courses_df, completed_courses):
    """
    Find semester courses the student is eligible to take.

    Completed courses are excluded, and remaining courses are checked against their
    prerequisite rules.

    Args:
        semester_courses_df (pandas.DataFrame): Available semester course offerings.
        completed_courses (list[str]): Course codes already completed by the student.

    Returns:
        pandas.DataFrame: Eligible course offerings with subject groups added.
    """
    eligible_rows = []

    for _, row in semester_courses_df.iterrows():
        course_code = row["course_code"]

        if course_code in completed_courses:
            continue

        if evaluate_prerequisite_rule(row["prerequisites"], completed_courses):
            eligible_rows.append(row)

    if not eligible_rows:
        return semester_courses_df.iloc[0:0]

    eligible_df = semester_courses_df.loc[[row.name for row in eligible_rows]]
    return add_course_groups(eligible_df)


def get_blocked_semester_courses(semester_courses_df, completed_courses):
    """
    Find semester courses blocked by unmet prerequisites.

    Args:
        semester_courses_df (pandas.DataFrame): Available semester course offerings.
        completed_courses (list[str]): Course codes already completed by the student.

    Returns:
        list[dict]: Blocked course records with a prerequisite reason.
    """
    blocked = []

    for _, row in semester_courses_df.iterrows():
        course_code = row["course_code"]

        if course_code in completed_courses:
            continue

        reason = missing_prerequisites(row["prerequisites"], completed_courses)

        if reason:
            item = row.to_dict()
            item["group"] = get_course_group(course_code)
            item["reason"] = reason
            blocked.append(item)

    return blocked


def elective_progress(elective_credits):
    """
    Calculate progress for each elective credit category.

    Args:
        elective_credits (dict): Completed elective credits by category.

    Returns:
        tuple: A list of elective progress dictionaries, total completed elective
        credits, and total required elective credits.
    """
    results = []
    total_completed = 0
    total_required = 0

    labels = {
        "general_elective_credits": "General Elective",
        "cs_elective_credits": "Computer Science Elective",
        "english_elective_credits": "English Elective",
        "science_elective_credits": "Science Elective",
        "humanities_elective_credits": "Humanities Elective",
        "social_science_elective_credits": "Social Science Elective",
        "ethics_elective_credits": "Ethics Elective"
    }

    for key, required in ELECTIVE_REQUIREMENTS.items():
        completed = int(elective_credits.get(key, 0))
        capped_completed = min(completed, required)
        remaining = max(required - completed, 0)
        percent = round((capped_completed / required) * 100, 1) if required else 0

        total_completed += capped_completed
        total_required += required

        results.append({
            "key": key,
            "category": labels[key],
            "completed": completed,
            "required": required,
            "remaining": remaining,
            "percent": percent
        })

    return results, total_completed, total_required


def required_progress(required_courses_df, completed_required_courses, elective_credits):
    """
    Calculate required-course, elective, and total degree progress.

    Args:
        required_courses_df (pandas.DataFrame): Required course catalog data.
        completed_required_courses (list[str]): Required course codes completed by the user.
        elective_credits (dict): Completed elective credits by category.

    Returns:
        dict: Degree progress summary, elective details, and remaining required courses.
    """
    total_required_credits = int(required_courses_df["credits"].sum())
    completed_df = required_courses_df[required_courses_df["course_code"].isin(completed_required_courses)]
    completed_required_credits = int(completed_df["credits"].sum())

    elective_details, completed_elective_credits, total_elective_required = elective_progress(elective_credits)

    total_completed_credits = completed_required_credits + completed_elective_credits
    total_degree_demo_credits = total_required_credits + total_elective_required

    remaining_df = required_courses_df[~required_courses_df["course_code"].isin(completed_required_courses)]

    required_percent = round((completed_required_credits / total_required_credits) * 100, 1) if total_required_credits else 0
    total_percent = round((total_completed_credits / total_degree_demo_credits) * 100, 1) if total_degree_demo_credits else 0

    remaining_df = add_course_groups(remaining_df)

    return {
        "completed_required_credits": completed_required_credits,
        "completed_elective_credits": completed_elective_credits,
        "total_completed_credits": total_completed_credits,
        "total_required_credits": total_required_credits,
        "total_elective_required": total_elective_required,
        "total_degree_demo_credits": total_degree_demo_credits,
        "required_percent": required_percent,
        "total_percent": total_percent,
        "elective_details": elective_details,
        "remaining_required_courses": remaining_df.to_dict(orient="records")
    }


def time_to_minutes(time_text):
    """
    Convert a time string into minutes after midnight.

    Supports 24-hour time such as `13:30` and 12-hour time such as `03:30pm`.

    Args:
        time_text (str): Time value to convert.

    Returns:
        int | None: Minutes after midnight, or None if the value cannot be parsed.
    """
    time_text = str(time_text).strip().lower()

    if time_text == "" or time_text == "nan":
        return None

    for fmt in ("%H:%M", "%I:%M%p", "%I:%M %p"):
        try:
            time_object = datetime.strptime(time_text, fmt)
            return time_object.hour * 60 + time_object.minute
        except ValueError:
            continue

    return None


def days_overlap(days_1, days_2):
    """
    Check whether two course meeting-day lists share at least one day.

    Args:
        days_1 (list): First course meeting days.
        days_2 (list): Second course meeting days.

    Returns:
        bool: True if the courses meet on at least one common day.
    """
    return any(day in days_2 for day in days_1)


def courses_conflict(course_1, course_2):
    """
    Determine whether two course sections have a schedule conflict.

    Two courses conflict when they meet on at least one shared day and their meeting
    times overlap.

    Args:
        course_1 (dict): First selected course section.
        course_2 (dict): Second selected course section.

    Returns:
        bool: True if the course sections overlap; False otherwise.
    """
    if not days_overlap(course_1["days"], course_2["days"]):
        return False

    first_start = time_to_minutes(course_1["start_time"])
    first_end = time_to_minutes(course_1["end_time"])
    second_start = time_to_minutes(course_2["start_time"])
    second_end = time_to_minutes(course_2["end_time"])

    if None in [first_start, first_end, second_start, second_end]:
        return False

    return first_start < second_end and second_start < first_end


def find_conflicts(selected_courses_df):
    """
    Find all pairwise schedule conflicts among selected courses.

    Args:
        selected_courses_df (pandas.DataFrame): Selected course sections.

    Returns:
        list[dict]: Conflicting course-section pairs.
    """
    conflicts = []
    rows = list(selected_courses_df.iterrows())

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            _, course_1 = rows[i]
            _, course_2 = rows[j]

            if courses_conflict(course_1, course_2):
                conflicts.append({
                    "course_1": f'{course_1["course_code"]}-{course_1["section"]}',
                    "course_2": f'{course_2["course_code"]}-{course_2["section"]}'
                })

    return conflicts


def check_schedule(semester_courses_df, selected_course_sections):
    """
    Build a selected schedule and report total credits and conflicts.

    Args:
        semester_courses_df (pandas.DataFrame): Available semester course offerings.
        selected_course_sections (list[str]): Selected CRNs or course-section IDs.

    Returns:
        dict: Selected schedule records, total credits, and detected conflicts.
    """
    semester_courses_df = semester_courses_df.copy()
    if "crn" in semester_courses_df.columns:
        semester_courses_df["course_section"] = semester_courses_df["crn"].astype(str)
    else:
        semester_courses_df["course_section"] = (
            semester_courses_df["course_code"].astype(str) + "-" + semester_courses_df["section"].astype(str)
        )

    selected_courses_df = semester_courses_df[semester_courses_df["course_section"].isin(selected_course_sections)]
    selected_courses_df = add_course_groups(selected_courses_df)

    conflicts = find_conflicts(selected_courses_df)
    total_credits = int(selected_courses_df["credits"].sum())

    return {
        "schedule": selected_courses_df.to_dict(orient="records"),
        "total_credits": total_credits,
        "conflicts": conflicts
    }


