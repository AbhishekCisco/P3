# College Management API

## Overview

This FastAPI project is a small REST API for organizing college departments and students. It demonstrates how request data moves through API routes, Pydantic schemas, SQLAlchemy models, and a local SQLite database. It is an introductory backend exercise in DAY1, alongside the separate Flask and raw-SQL examples.

## Learning Objectives

- Start a FastAPI application and explore its interactive API documentation.
- Define database tables and relationships with SQLAlchemy ORM models.
- Validate request bodies and shape responses with Pydantic schemas.
- Inject and close database sessions through FastAPI dependencies.
- Create related records and return useful errors when a referenced department does not exist.

## Topics Covered

- **REST endpoints:** `GET` routes list departments and students; `POST` routes create them.
- **Relational data:** each student belongs to a department through `department_id`, and SQLAlchemy relationships expose the linked department name.
- **Validation and serialization:** Pydantic checks incoming field types and response models serialize ORM objects.
- **Dependency injection:** `get_db()` provides a session to a route and closes it after the request.
- **SQLite persistence:** data is stored in `college.db`, a local database file.

## Project Structure

```text
college_management_api/
├── routers/
│   ├── departments.py  # Department list and create endpoints
│   └── students.py     # Student list and create endpoints
├── database.py         # SQLite engine, session factory, and dependency
├── main.py             # FastAPI app, table creation, and router registration
├── models.py           # Department and Student ORM models
├── schemas.py          # Request and response schemas
├── requirements.txt    # Runtime dependencies
├── college.db          # SQLite database (created when the app starts)
└── README.md
```

## How the Files Work Together

`main.py` creates the tables from the models and registers the department and student routers. Each router receives a SQLAlchemy `Session` from `database.get_db()`. The route uses the models to query or write records, while the schemas validate request bodies and define response fields. The student list query eagerly loads each student's department so the response can include `department_name`.

The API currently supports:

| Method | Path | Behavior |
| --- | --- | --- |
| `GET` | `/` | Returns a simple running-status message. |
| `GET` | `/api/departments/` | Lists departments. |
| `POST` | `/api/departments/` | Creates a department from `department_name`. |
| `GET` | `/api/students/` | Lists students with their department names. |
| `POST` | `/api/students/` | Creates a student after confirming the department exists. |

## Setup and Run

Use Python 3.10 or newer. Run these commands from this project directory so the relative SQLite URL points to the local `college.db` file:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

On Windows PowerShell, activate the environment with `.venv\\Scripts\\Activate.ps1`.

Open `http://127.0.0.1:8000/docs` to try the endpoints through Swagger UI. Tables are created at startup, but the project has no seed-data script; create a department before creating a student, then use its returned ID as `department_id`.

## Expected Behavior and Limitations

- Creating a student for an unknown department returns HTTP `404` with `Department not found`.
- Invalid or missing required request fields are rejected by FastAPI/Pydantic with a validation response.
- The project has no automated tests, authentication, update/delete endpoints, pagination, or migration setup.
- Database creation uses `Base.metadata.create_all()` at import/startup. This is convenient for a learning example but does not replace versioned migrations for a maintained application.
- The SQLite URL is relative to the current working directory, so start Uvicorn from this folder.

## What to Study Next

Add focused API tests with FastAPI's `TestClient`, then explore database migrations, uniqueness constraints, pagination, and update/delete operations. Keep request schemas separate from database models as the API grows.