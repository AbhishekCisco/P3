# College Departments and Students with Flask and SQLite

## Overview

This small Flask API demonstrates reading related department and student records from SQLite and returning JSON. It is the raw-SQL counterpart to the SQLAlchemy-based College Management API in the neighboring DAY1 folder.

## Learning Objectives

- Connect Python code to a local SQLite database.
- Create tables and insert seed rows with parameterized SQL.
- Join related tables and return the results as JSON.
- Understand why the current database initializer replaces its tables.

## Topics Covered

- **SQLite and SQL:** `init_db.py` creates the `departments` and `students` tables and inserts sample rows.
- **Relational joins:** `/studentDepartments` uses a `LEFT JOIN` so a student can still appear if there is no matching department.
- **Flask routes:** `boilerCode.py` exposes read-only JSON endpoints.
- **Resource cleanup:** route handlers close their SQLite connection after reading.

## Project Structure

```text
college management API/
├── boilerCode.py    # Flask app and JSON endpoints
├── connection.py    # SQLite connection helper
├── init_db.py       # Recreates tables and inserts sample data
├── requirements.txt # Flask dependency
├── studentDB.db     # SQLite database used by the examples
└── README.md
```

## How the Files Work Together

`connection.py` opens `studentDB.db` relative to the current working directory. `init_db.py` uses that helper to create five departments and five students. `boilerCode.py` uses the same helper to query the tables and convert each row into a JSON object.

| Method | Path | Behavior |
| --- | --- | --- |
| `GET` | `/departments` | Returns department IDs and names. |
| `GET` | `/studentDepartments` | Returns student names and their department names. |

## Setup and Run

Use Python 3. Run these commands from this project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python init_db.py
python boilerCode.py
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. Visit `http://127.0.0.1:5000/departments` or `http://127.0.0.1:5000/studentDepartments` to see the JSON responses. There is no root route, so `/` is not the API's example endpoint.

## Expected Behavior and Limitations

- The initializer drops and recreates both tables each time it runs. It is a sample-data reset, not a safe production migration; any custom rows in those tables are lost.
- The API provides reads only; it has no endpoints for adding or changing records.
- There are no automated tests or authentication. The Flask development server runs with debug mode enabled.
- The database path is relative to the working directory. Start the script from this folder so it uses the intended database file.

## What to Study Next

Compare this project's explicit SQL and tuple-to-JSON conversion with the neighboring FastAPI/SQLAlchemy project. Add tests for empty tables, missing department references, and the expected join results before adding write endpoints.