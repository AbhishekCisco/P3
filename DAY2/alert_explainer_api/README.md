# Alert Explainer API

## Overview

This FastAPI application stores monitoring alerts in SQLite and returns a plain-language explanation of an alert's metric and severity. It is a backend and API-testing exercise in DAY2. Despite the title, the explanation is produced by deterministic Python rules; this project does not call an AI model.

## Learning Objectives

- Build create, list, and detail endpoints with FastAPI.
- Validate request bodies with Pydantic and persist ORM objects with SQLAlchemy.
- Separate HTTP routing from explanation logic in a service module.
- Replace the production database dependency with an isolated in-memory database for tests.

## Topics Covered

- **REST and status codes:** alert creation returns `201`, missing alerts return `404`, and invalid request fields are rejected by Pydantic.
- **Data modeling:** each alert stores its title, severity, source, metric value, threshold, and creation time.
- **Rule-based explanations:** `generate_explanation()` compares a metric with its threshold and selects suggested next steps by severity.
- **Automated API tests:** tests use FastAPI's `TestClient` and a temporary in-memory SQLite database.

## Project Structure

```text
alert_explainer_api/
├── routers/
│   └── alerts.py       # Alert CRUD-like reads/creation and explain route
├── services/
│   └── explainer.py    # Deterministic explanation text
├── database.py        # SQLite engine, session factory, and dependency
├── main.py            # App creation, table setup, and router registration
├── models.py          # SQLAlchemy Alert model
├── schemas.py         # Pydantic request/response models
├── test_alerts.py     # API tests using an isolated database
├── requirements.txt   # Runtime dependencies
├── alerts.db          # Local SQLite database
└── README.md
```

## How the Files Work Together

`main.py` creates the alert table and registers the router. Routes obtain a database session from `database.get_db()`, use `models.Alert` for persistence, and validate output with `schemas.py`. The explain route passes an alert to `services/explainer.py`; that service selects wording based on whether the metric is above, below, or equal to its threshold.

Available routes are `POST /alerts/` to create an alert, `GET /alerts/` to list alerts, `GET /alerts/{alert_id}` to fetch one, and `POST /alerts/{alert_id}/explain` to generate its explanation. `GET /` reports whether the API is running.

## Setup and Run

Use Python 3.10 or newer. From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. Open `http://127.0.0.1:8000/docs` to create an alert and try its explanation route. The app creates its SQLite table at startup.

To run the tests, install the test-only packages as well (`pytest` and `httpx` are imported by the test setup but are not listed in `requirements.txt`), then run `python -m pytest -q` from this folder. Tests replace the file-backed database with an in-memory one.

## Expected Behavior and Limitations

- An unknown alert ID returns HTTP `404`.
- Severity is restricted to `critical`, `warning`, or `info` by the request schema.
- Explanations are fixed templates, not model-generated advice; they should not be treated as operational decisions without human review.
- There is no authentication, authorization, update/delete endpoint, pagination, or database migration tooling.
- Test dependencies are not declared in `requirements.txt`.

## What to Study Next

Add tests for invalid severity and exact-threshold behavior, then compare these deterministic service rules with an LLM-backed explainer while keeping factual alert data and recommendations clearly separated.