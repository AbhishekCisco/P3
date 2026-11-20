# FastAPI Runtime Debugging Lab

## Overview

This lab demonstrates a structured workflow for reproducing, explaining, fixing, and testing three common Python runtime errors in a small employee API. The current implementation contains the fixes and tests; the lab document also describes the original faulty examples and Copilot prompts.

## Learning Objectives

- Recognize type errors, missing dictionary keys, and division by zero.
- Return meaningful HTTP responses for invalid or missing data.
- Use FastAPI's test client to verify both successful and error cases.
- Ask for a root-cause explanation before accepting a code change.

## Topics Covered

- **FastAPI routing and parameters:** query parameters control the salary-average example, and path parameters identify employees.
- **Defensive code:** salary text is converted to a number, missing dictionary entries return `404`, and non-positive employee counts return `400`.
- **Automated tests:** five tests cover the bonus, existing/missing employee, and valid/zero-count average cases.
- **AI-assisted debugging:** `lab_desc.md` gives prompts and a reproduce-explain-fix-validate workflow.

## Project Structure

```text
copilot-runtime-debugging/
├── test/
│   └── test_main.py # FastAPI TestClient tests
├── lab_desc.md      # Full guided debugging exercise
├── main.py          # Fixed API examples
├── requirements.txt # FastAPI, Uvicorn, pytest, and httpx
└── README.md
```

## How the Files Work Together

`main.py` defines the app and its `/employee/bonus`, `/employee/{employee_id}`, and `/employee/average-salary` routes. `test/test_main.py` calls the app in process using `TestClient` and asserts response bodies and status codes. The `Employee` Pydantic model is declared but is not currently used by these routes.

## Setup and Run

Use Python 3.10 or newer. From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. Open `http://127.0.0.1:8000/docs` to inspect the API. In another terminal, run the tests from this folder with `python -m pytest -q`.

The bonus endpoint returns `5000.0`. The average endpoint defaults to a total of `150000` and a count of `8`; a non-positive count returns HTTP `400`. Employee `101` exists, while an unknown ID returns HTTP `404`.

## Current Status and Limitations

- The source and tests reflect the fixed implementation, while `lab_desc.md` teaches from intentionally broken versions. Reproduce the original errors using the examples in the guide, not by assuming the current `main.py` still contains them.
- Employee records are hard-coded; there is no database or persistence.
- The API has no authentication, write operations, or tests for every possible input boundary.

## What to Study Next

Compare direct function-level tests with endpoint tests, then add cases for malformed numeric values and boundary employee counts. Keep user-facing HTTP errors distinct from unexpected server failures.