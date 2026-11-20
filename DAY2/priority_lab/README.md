# Alert Priority Scoring Lab

## Overview

This exercise combines a small priority-scoring function with a FastAPI endpoint backed by SQLite. Given an existing alert, the endpoint calculates a score from its severity, metric value, and threshold. The folder focuses on unit testing, API error handling, and test-fixture design.

## Learning Objectives

- Read and test a standalone scoring function.
- Connect a FastAPI endpoint to a SQLAlchemy model and database session.
- Translate domain errors into HTTP status codes.
- Recognize the importance of runnable fixtures and reproducible test data.

## Topics Covered

- **Scoring logic:** `priority_score.py` assigns severity weights (`critical` 60, `warning` 30, `info` 10) and adds a threshold-breach bonus capped at 40 points.
- **Validation:** unsupported severity and a zero threshold raise `ValueError`.
- **Persistence:** `main.py` looks up an `Alert` record from SQLite before calculating its score.
- **API errors:** an unknown alert ID returns `404`; scoring input errors become `422` responses.
- **Testing:** the unit and integration test files are intended to cover calculation and HTTP behavior, but the current test code is incomplete or malformed.

## Project Structure

```text
priority_lab/
├── database.py          # SQLite engine, session factory, and dependency
├── main.py              # Table setup and GET priority endpoint
├── models.py            # Alert ORM model
├── priority_score.py    # Severity and threshold calculation
├── test_priority.py     # Unit tests for scoring edge cases
├── test_integration.py  # Intended endpoint tests
├── alerts.db            # Created at startup; no seed script is included
└── README.md
```

## How the Files Work Together

At startup `main.py` creates the `alerts` table from `models.Alert`. The route `GET /alerts/{alert_id}/priority` fetches one row using the injected session, calls `calculate_priority_score()`, then returns `alert_id` and `priority_score`. The application has no endpoint for creating alerts, so an empty database returns `404` for every alert ID until a record is added separately.

## Setup and Run

There is no `requirements.txt`. Use Python 3 and install FastAPI, Uvicorn, SQLAlchemy, and the test tools (`pytest` and `httpx`) in a virtual environment. From this folder, run the app with:

```bash
uvicorn main:app --reload
```

The endpoint is documented at `http://127.0.0.1:8000/docs`. Running `python -m pytest -q` is the intended test command after dependencies and valid test fixtures are available.

## Current Issues and Limitations

- No seed script or alert-creation endpoint is provided; the API cannot demonstrate a successful lookup with a fresh database by itself.
- Several earlier parameterized tests in `test_priority.py` and most of `test_integration.py` are commented out. The remaining unit-test indentation appears invalid, and the live integration test refers to a `test_context` fixture and `Alert` name that are not defined in its active code. The suite should be repaired before relying on its results.
- There is no authentication, update/delete route, pagination, or migration setup.
- The scoring rule is an educational example; the severity weights and bonus formula have no documented operational calibration.

## What to Study Next

First make each test module independently collectable with an isolated in-memory database fixture. Then define seed data and boundary cases for a metric at, below, and above its threshold, including negative values and the capped bonus.