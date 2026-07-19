# Developer Manual

## Architecture
The project uses a client/server design:
- Streamlit provides the user interface.
- FastAPI provides backend endpoints and planning services.
- The transcript parser extracts completed courses from PDF and DOCX files.
- The planner evaluates degree requirements, prerequisites, and schedule conflicts.
- The curriculum AI module generates semester recommendations.
- Data-manager and model modules provide shared data access and typed structures.

## Expected Backend Modules
- `main.py`
- `auth.py`
- `planner.py`
- `data_manager.py`
- `models.py`
- `transcript_parser.py`
- `curriculum_ai.py`

## Expected Frontend Modules
- `login.py`
- `ui.py`
- `data.py`
- `pages/courseselection.py`
- `pages/schedule.py`
- utility modules under `frontend/util/`

## Transcript Parsing Rules
The parser:
1. Extracts text.
2. Removes the `COURSE(S) IN PROGRESS` section.
3. Combines wrapped course rows.
4. validates subject and course-number pairs.
5. identifies the grade near the credit values.
6. includes passing grades.
7. excludes failed, withdrawn, and co-op courses.

## Configuration
Environment variables should be stored in `.env`, never committed with real secrets.

## Running Locally
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn backend.main:app --reload
streamlit run frontend/login.py
```

## Extending the System
- Add or update degree requirements through the data-manager layer.
- Add a new transcript format by extending the extraction and row-detection logic.
- Add API endpoints in FastAPI and consume them through the Streamlit data layer.
- Add persistent storage by replacing file-based storage with a relational database.
