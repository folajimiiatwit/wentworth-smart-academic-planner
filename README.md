# Wentworth Smart Academic Planner

The **Wentworth Smart Academic Planner** is a web-based application designed to help Wentworth Institute of Technology students plan their path to graduation. The application analyzes a student's completed coursework, tracks graduation progress, recommends future semesters using AI, and helps students build conflict-free class schedules.

---

## Features

### Login
- Simple username-based login
- Automatically loads previously saved student progress

### Transcript Upload
Students can upload an unofficial transcript in:

- PDF
- DOCX

The application automatically:

- Extracts transcript text
- Identifies completed courses
- Ignores semester headings (e.g., Fall 2025)
- Ignores courses listed under **Courses in Progress**
- Ignores withdrawn or failed courses
- Separates required courses from transfer/custom courses

### Manual Course Entry

If a completed course is not detected automatically, students can manually add:

- Course Code
- Course Number
- Course Title

### Degree Progress

The application displays:

- Completed required courses
- Remaining required courses
- Remaining elective credits by category
- Overall degree completion progress

Elective categories include:

- Computer Science
- General Education
- English
- Science
- Humanities
- Social Science
- Ethics

### Schedule Builder

Students can:

- View only courses whose prerequisites have been satisfied
- Select course sections
- Detect schedule conflicts
- View schedules in either:
  - Weekly calendar view
  - Table view

### AI Curriculum Map

Using OpenAI, the application generates a personalized semester-by-semester graduation plan based on:

- Completed required courses
- Completed elective credits
- Remaining graduation requirements

If all graduation requirements have already been completed, the application informs the student that no additional courses are needed.

---

# Project Structure

```
wentworth-smart-academic-planner/
│
├── backend/
│   ├── auth.py
│   ├── curriculum_ai.py
│   ├── data_manager.py
│   ├── main.py
│   ├── planner.py
│   ├── transcript_parser.py
│   └── data/
│
├── frontend/
│   ├── data.py
│   ├── login.py
│   ├── ui.py
│   ├── util/
│   │   ├── calendar_helpers.py
│   │   ├── course_helpers.py
│   │   └── course_selection_helpers.py
│   └── pages/
│       ├── courseselection.py
│       └── schedule.py
│
├── data/
├── assets/
│
├── documentation/
│   ├── Final_Design_and_Project_Report.pdf
│   ├── Final_Design_and_Project_Report.docx
│   ├── User_Manual.md
│   ├── Developer_Manual.md
│   ├── Project_Goals_Evaluation.md
│   ├── Known_Issues_and_Limitations.md
│   ├── diagrams/
│   ├── testing/
│   ├── notes/
│   └── presentation/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── terminal_demo.py
```

# Project Documentation

The final project documentation is available in the
[`documentation`](documentation/) folder.

## Main Documents

- [Final Design and Project Report — PDF](documentation/Final_Design_Document_and_Project_Report.pdf)
- [Final Design and Project Report — DOCX](documentation/Final_Design_Document_and_Project_Report.docx)
- [User Manual](documentation/User_Manual.md)
- [Developer Manual](documentation/Developer_Manual.md)
- [Project Goals Evaluation](documentation/Project_Goals_Evaluation.md)
- [Known Issues and Limitations](documentation/Known_Issues_and_Limitations.md)
- [Testing Report](documentation/testing/Testing_Report.md)

## Design Diagrams

- [System Architecture](documentation/diagrams/System_Architecture.png)
- [Component Diagram](documentation/diagrams/Component_Diagram.png)
- [Transcript Processing Workflow](documentation/diagrams/Transcript_Workflow.png)
- [Use Case Diagram](documentation/diagrams/Use_Case_Diagram.png)
- [Class Diagram](documentation/diagrams/Class_Diagram.png)

## Project Notes

- [Interesting and Unexpected Findings](documentation/notes/Interesting_Unexpected_and_Confusing_Items.md)
- [Lessons Learned](documentation/notes/Lessons_Learned.md)

## Presentation

- [Final Project Presentation](documentation/presentation/Final_Presentation.pptx)

---

# Technologies Used

## Frontend

- Streamlit
- streamlit-calendar

## Backend

- FastAPI
- Uvicorn

## Data Processing

- pandas
- pdfplumber
- python-docx

## Artificial Intelligence

- OpenAI GPT-4o API

---

# Installation

Clone the repository.

```bash
git clone https://github.com/folajimiiatwit/wentworth-smart-academic-planner.git
```

Move into the project directory.

```bash
cd wentworth-smart-academic-planner
```

Install the required packages.

```bash
pip install -r requirements.txt
```

---

# OpenAI Setup

Create a `.env` file in the project root.

```text
OPENAI_API_KEY=your_api_key_here
```

The AI Curriculum Map feature requires an OpenAI API key.

---

# Running the Application

Run the frontend.

```bash
python -m streamlit run frontend/login.py
```

The frontend automatically starts the backend if it is not already running.

Alternatively, you can start the backend manually.

```bash
python -m uvicorn backend.main:app --reload
```

The Application can also be accessed through this [link](https://wentworth-smart-academic-planner.onrender.com/)

---

# How to Use

1. Log in with your username.
2. Upload an unofficial transcript.
3. Review automatically detected completed courses.
4. Add any missing completed courses manually.
5. Enter completed elective credits.
6. Save your completed information.
7. Review your graduation progress.
8. Generate an AI Curriculum Map.
9. Build your semester schedule.
10. View your schedule in the interactive calendar.

---

# Backend API

| Endpoint | Description |
|----------|-------------|
| `/login` | User login |
| `/required-courses` | Retrieve required courses |
| `/eligible-courses/{username}` | Retrieve eligible courses |
| `/blocked-courses/{username}` | Retrieve blocked courses |
| `/check-schedule` | Detect schedule conflicts |
| `/save-completed-info` | Save completed required courses |
| `/save-custom-completed` | Save custom completed courses |
| `/progress/{username}` | Retrieve graduation progress |
| `/parse-transcript` | Parse uploaded transcript |
| `/curriculum-map` | Generate AI curriculum map |
| `/health` | Backend health check |

---

# Design Highlights

- Separation of frontend and backend using REST APIs.
- Automatic transcript parsing to reduce manual data entry.
- Personalized degree progress tracking.
- AI-assisted semester planning.
- Interactive schedule builder with conflict detection.
- Modular frontend architecture using reusable helper modules.

---

# Future Improvements

- Support additional academic programs.
- Integrate directly with Wentworth's student information system.
- Add advisor approval workflows.
- Recommend courses across multiple future semesters.
- Authentication using Wentworth credentials.

---

# Contributors

**Ibukunoluwa Folajimi**
- Backend development
- Transcript parser
- AI Curriculum Map
- Degree progress tracking

**Ben Le**
- Frontend development
- User interface
- Backend/frontend integration
- Calendar integration
- Schedule visualization

---
