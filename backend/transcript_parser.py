"""
Purpose:
Extracts completed courses from uploaded transcript files.

Main responsibilities:
- Extract text from PDF, DOCX, and TXT transcripts (Currently TXT is not working and won't be made avaliable to upload)
- Ignore courses listed under COURSE(S) IN PROGRESS
- Ignore failed or withdrawn courses
- Identify completed course codes
- Separate required courses from custom or transfer courses
"""
import re
from io import BytesIO
from docx import Document
import pdfplumber

PASSING_GRADES = {
    "A","A-",
    "B+","B","B-",
    "C+","C","C-",
    "D+","D","S","TR"
}

FAILING_GRADES = {
    "F", "W", "D-"

}

SEMESTER_WORDS = {
    "FALL", "SPRING", "SUMMER", "WINTER", "TERM", "YEAR"
}

NON_COURSE_WORDS = {
    "GPA", "UG", "CEU", "WEB", "TOP", "THE", "AND", "FOR", "NOT",
    "TOTAL", "TOTALS", "CURRENT", "CUMULATIVE", "OVERALL"
}

STOP_MARKERS = [
    "COURSE(S) IN PROGRESS",
    
]


def extract_text_from_docx(file_bytes):
    """
    Extract transcript text from a DOCX file.

    Both paragraph text and table cell text are included because transcripts may store
    course information in either format.

    Args:
        file_bytes (bytes): Raw DOCX file content.

    Returns:
        str: Extracted transcript text.
    """
    document = Document(BytesIO(file_bytes))
    parts = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            parts.append(text)

    for table in document.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if any(cells):
                parts.append("\t".join(cells))

    return "\n".join(parts)


def extract_text_from_pdf(file_bytes):
    """
    Extract transcript text from a PDF file using pdfplumber.

    Args:
        file_bytes (bytes): Raw PDF file content.

    Returns:
        str: Extracted transcript text from all readable pages.
    """

    parts = []

    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                parts.append(text)

    return "\n".join(parts)


def extract_text_from_txt(file_bytes):
    """
    Extract transcript text from a plain-text file.

    Args:
        file_bytes (bytes): Raw TXT file content.

    Returns:
        str: Decoded transcript text.
    """
    return file_bytes.decode("utf-8", errors="ignore")


def extract_text_from_file(filename, file_bytes):
    """
    Select the correct transcript text extractor based on file extension.

    Supported extensions include `.docx`, `.pdf`, and `.txt`. Unknown file types are
    processed as plain text.

    Args:
        filename (str): Uploaded transcript filename.
        file_bytes (bytes): Raw uploaded file content.

    Returns:
        str: Extracted transcript text.
    """
    filename = filename.lower()

    if filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if filename.endswith(".txt"):
        return extract_text_from_txt(file_bytes)

    return extract_text_from_txt(file_bytes)


def remove_in_progress_section(text):
    """
    Remove transcript sections that list courses currently in progress.

    Courses after the configured stop marker should not count as completed courses.

    Args:
        text (str): Full transcript text.

    Returns:
        str: Transcript text before any in-progress section.
    """
    upper_text = text.upper()

    cut_positions = []
    for marker in STOP_MARKERS:
        position = upper_text.find(marker)
        if position != -1:
            cut_positions.append(position)

    if not cut_positions:
        return text

    return text[:min(cut_positions)]


def normalize_lines(text):
    """
    Convert transcript text into a clean list of non-empty lines.

    Args:
        text (str): Raw transcript text.

    Returns:
        list[str]: Trimmed non-empty transcript lines.
    """
    lines = []

    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned:
            lines.append(cleaned)

    return lines


def is_valid_subject(subject):
    """
    Check whether a detected subject prefix looks like a real course subject.

    Semester words and common non-course words are rejected to reduce false matches.

    Args:
        subject (str): Candidate course subject prefix.

    Returns:
        bool: True if the subject appears valid.
    """
    subject = subject.strip().upper()

    if not re.fullmatch(r"[A-Z]{3,5}", subject):
        return False

    if subject in SEMESTER_WORDS:
        return False

    if subject in NON_COURSE_WORDS:
        return False

    return True


def looks_like_course_number(value):
    """
    Check whether a value looks like a four-digit course number.

    Args:
        value (str): Candidate course number.

    Returns:
        bool: True if the value is exactly four digits.
    """
    return bool(re.fullmatch(r"\d{4}", value.strip()))


def is_valid_course_pair(subject, number):
    """
    Validate a subject and course-number pair before treating it as a course.

    This prevents transcript headings such as `FALL 2025` from being mistaken for
    course codes.

    Args:
        subject (str): Candidate course subject.
        number (str): Candidate four-digit course number.

    Returns:
        bool: True if the pair appears to represent a course.
    """
    subject = subject.strip().upper()
    number = number.strip()

    if not is_valid_subject(subject):
        return False

    if not looks_like_course_number(number):
        return False

    # Extra safety: do not treat semester years as course numbers.
    if subject in SEMESTER_WORDS and number.startswith("20"):
        return False

    return True


def extract_completed_courses_from_text(text):
    """
    Extract completed course codes from transcript text.

    Only courses with passing grades are included. Courses in progress, failed
    courses, withdrawn courses, and semester headings are ignored.

    Args:
        text (str): Extracted transcript text.

    Returns:
        list[str]: Sorted completed course codes.
    """
    completed = set()
    safe_text = remove_in_progress_section(text)
    safe_text_upper = safe_text.upper()

    grade_pattern = r"(A-|A|B\+|B-|B|C\+|C-|C|D\+|D|TR|P|S|F|W|WF|WU|NC|I|D-)"

    lines = normalize_lines(safe_text_upper)

    for line in lines:
        match = re.search(r"\b([A-Z]{3,5})\s+(\d{4})\b", line)

        if not match:
            continue

        subject = match.group(1)
        number = match.group(2)

        if not is_valid_course_pair(subject, number):
            continue

        grade_matches = re.findall(rf"\b{grade_pattern}\b", line)

        if not grade_matches:
            continue

        grade = grade_matches[-1].upper()

        if grade in PASSING_GRADES:
            completed.add(f"{subject}{number}")

    return sorted(completed)


def split_required_and_custom(extracted_codes, required_course_codes):
    """
    Separate extracted transcript courses into required and custom completed courses.

    Args:
        extracted_codes (list[str]): Course codes found in the transcript.
        required_course_codes (list[str]): Required course codes for the program.

    Returns:
        tuple: Completed required course codes and custom completed course records.
    """
    required_set = set(str(code).strip().upper() for code in required_course_codes)

    completed_required = []
    custom_completed = []

    for code in extracted_codes:
        code = str(code).strip().upper()

        if code in required_set:
            completed_required.append(code)
        else:
            subject_match = re.match(r"([A-Z]+)(\d+)", code)

            if subject_match:
                number = subject_match.group(2)
            else:
                number = ""

            custom_completed.append({
                "course_code": code,
                "course_number": number,
                "title": "Imported from transcript"
            })

    return completed_required, custom_completed
