# Wentworth Smart Academic Planner

The Wentworth Smart Academic Planner is a web-based application designed to help Wentworth Institute of Technology Computer Science students track degree progress and plan their path to graduation.

The application uses a Streamlit frontend and FastAPI backend. Students can upload unofficial transcripts, review completed coursework, track remaining graduation requirements, build conflict-free schedules, and generate AI-assisted semester plans.

Student accounts and saved academic progress are stored in a relational database using SQLAlchemy. SQLite is used for local development, while PostgreSQL is supported for deployed environments.

---

## Features

### Login and Saved Progress

- Simple username-based prototype login
- Creates a user database record when a new username is entered
- Automatically loads previously saved:
  - Completed required courses
  - Custom or transfer courses
  - Elective credit totals
- Preserves user progress between sessions when persistent database storage is configured

> The current login system is intended for demonstration purposes and does not use passwords or institutional authentication.

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
│   ├── database.py
│   ├── database_models.py
│   ├── data_manager.py
│   ├── main.py
│   ├── planner.py
│   └── transcript_parser.py
│
├── data/
│   ├── cs_required_courses.csv
│   ├── semester_courses.csv
│   ├── migrate_users_to_database.py
│   └── users.csv
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
├── assets/
├── .env.example
├── .gitignore
├── requirements.txt
├── terminal_demo.py
└── README.md
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

## Database and Persistence

- SQLAlchemy
- SQLite for local development
- PostgreSQL for deployed environments
- Psycopg PostgreSQL driver
- Neon PostgreSQL hosting

## Data Processing

- pandas
- pdfplumber
- python-docx

## Artificial Intelligence

- OpenAI GPT-4o API

## Version Control and Deployment

- GitHub
- Render

---

# Installation

Clone the repository:

```bash
git clone https://github.com/folajimiiatwit/wentworth-smart-academic-planner.git
cd wentworth-smart-academic-planner
```
---

# Environment Configuration

Copy `.env.example` to a local `.env` file:

```bash
cp .env.example .env
```

The AI Curriculum Map feature requires an OpenAI API key.

---
# Running the Application

## Option 1: Start the frontend

```bash
python -m streamlit run frontend/login.py
```

The frontend automatically starts the backend if it is not already running.

## Option 2: Start the services separately

Backend:

```bash
python -m uvicorn backend.main:app --reload
```

Frontend, in a second terminal:

```bash
python -m streamlit run frontend/login.py
```

The FastAPI documentation is available locally at:

```text
http://127.0.0.1:8000
```

# Deployment

The application has be deployed using:

- Render for the FastAPI and Streamlit services
- Neon for hosted PostgreSQL storage

In Render, configured are the following environment variables:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=our_neon_postgresql_connection_string
```

The Application can also be accessed through this [link](https://wentworth-smart-academic-planner.onrender.com/)

---

# Data Storage

The application uses two forms of storage.

## Static Academic Data

CSV files continue to store institutional reference data:

- Required Computer Science courses
- Semester course offerings
- Prerequisite and scheduling information

## User-Generated Data

A relational database stores:

- Usernames
- Completed required courses
- Custom or transfer courses
- Elective credit totals
- Planned-course information

The frontend does not communicate directly with the database. It sends requests to FastAPI, and the backend uses SQLAlchemy to retrieve or update database records.

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

- Separation of the Streamlit frontend and FastAPI backend through REST APIs
- SQLAlchemy-based persistence layer
- SQLite support for local development
- PostgreSQL support for deployed environments
- Automatic creation and retrieval of user records
- Automatic transcript parsing to reduce manual data entry
- Personalized degree-progress tracking
- AI-assisted semester planning
- Interactive schedule builder with conflict detection
- Modular frontend architecture using reusable helper modules

# Security and Privacy

The current application uses username-only authentication and is intended as an academic prototype.

It should not be used with official student records or sensitive educational data without additional security controls, including:

- Password-based or institutional authentication
- Wentworth Single Sign-On
- Authorization controls
- HTTPS
- Secure secrets management
- FERPA-aligned data handling
- Audit logging
- Database backups

Unofficial transcripts should be used only with the student's permission.

---

# Future Improvements

- Add password-based authentication or Wentworth Single Sign-On
- Integrate with Wentworth's Banner Student Information System
- Normalize completed courses into separate relational database tables
- Support additional academic programs
- Add advisor review and approval workflows
- Add role-based access control
- Encrypt sensitive student information
- Add automated database backups
- Add account deletion and data-export features
- Expand transcript compatibility
- Add automated testing and continuous deployment

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
