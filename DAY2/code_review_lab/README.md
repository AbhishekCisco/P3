# Alert Utilities Code Review Lab

## Overview

This exercise reviews small alert-formatting and database-query helpers, with a focus on input validation and SQL injection prevention. It pairs a demonstration script with pytest checks and is intended for code-review practice rather than deployment as an alerting service.

## Learning Objectives

- Trace how helper functions validate and format alert information.
- Recognize parameterized SQL and understand why it treats input as data.
- Use focused tests to check normal behavior and suspicious input.
- Inspect side effects before running a database demonstration.

## Topics Covered

- **Input validation:** the source name must be a non-empty string, and alert levels are restricted to `CRITICAL` and `WARNING`.
- **SQL injection defense:** `get_alerts_by_source()` binds the source as a query parameter instead of inserting it into SQL text.
- **Threshold-based messaging:** a page-on-call sentence is added only when a metric exceeds 150% of its threshold.
- **Regression tests:** the tests verify message text, invalid levels, blank input, and that an injection-shaped value does not return all rows.

## Project Structure

```text
code_review_lab/
├── alert_utils.py       # Formatting and parameterized SQLite lookup
├── check_injection.py   # Builds a demo table and compares lookup inputs
├── test_alert_utils.py  # Pytest checks
├── alerts_demo.db       # SQLite file used by the demonstration script
└── README.md
```

## How the Files Work Together

`alert_utils.py` contains both the pure message formatter and the SQLite lookup. `test_alert_utils.py` creates an isolated temporary database for its query tests, so the tests do not need to use the demo database. `check_injection.py` creates a small table and passes both a normal source and an injection-shaped string through the helper.

## Setup and Run

The utility code uses the Python standard library. Install pytest to run the test suite:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. To see the message-formatting example, run `python alert_utils.py`. The database demonstration is `python check_injection.py`.

## Expected Behavior and Limitations

- The SQL injection-shaped lookup value is treated literally and matches no rows in the test fixture.
- `check_injection.py` drops and recreates the `alerts` table in `alerts_demo.db` each time it runs. Do not use that file for data you need to preserve.
- `get_alerts_by_source()` does not close its SQLite connection after fetching rows; this is a resource-management issue to investigate in the exercise, not a change made here.
- `DB_PASSWORD` and `ADMIN_API_KEY` are read from the environment in the source but are not used by the current functions. No values are needed for these examples.
- The tests require pytest, which is not listed in a project dependency file.

## What to Study Next

Review connection lifetime and exception handling around SQLite operations. Add tests for the 150% threshold boundary and for unusual values before considering any production use.