# AI-Assisted Application Log Analysis

## Overview

This FastAPI demo and its seeded log file teach how to summarize operational events, group repeated errors, and validate AI-generated findings against raw evidence. The exercise emphasizes that a model's explanation is a hypothesis unless the log itself supports it.

## Learning Objectives

- Use structured prompts to summarize log activity and count events.
- Separate observations visible in logs from possible causes.
- Validate counts and timestamps against the original entries.
- Compare a fixed sample log with logs produced by a running application.

## Topics Covered

- **Python logging:** the app writes to the terminal and to a file under `logs/`.
- **FastAPI routes:** demo endpoints generate normal employee events and controlled error-pattern entries.
- **Evidence-based analysis:** the seeded `application.log` contains 18 entries: 6 INFO, 3 WARNING, and 9 ERROR records.
- **Operational caution:** retries and timeouts do not prove an operation succeeded or failed; verify transaction state before repeating an action.

## Project Structure

```text
ai-log-analysis/
├── logs/
│   ├── .gitkeep
│   └── application.log  # Runtime log destination; currently contains accumulated entries
├── application.log     # Fixed 18-entry sample used by the prompt exercise
├── lab_desc.md         # Prompts, expected analysis, and manual validation steps
├── main.py             # FastAPI demo and logging configuration
├── requirements.txt    # FastAPI and Uvicorn
└── README.md
```

## How the Files Work Together

`lab_desc.md` directs the learner to analyze the root-level `application.log` sample and verify the counts. `main.py` is a separate demo service: it configures logging to `logs/application.log`, serves health and employee routes, and exposes `GET /demo-log-errors` to write a controlled set of errors and warnings without crashing the API.

The two log files have different purposes. The root-level sample is the fixed dataset for reproducible prompting. The `logs/application.log` file is the runtime destination and can accumulate entries across runs. Do not substitute one for the other when comparing with the exercise's expected counts.

## Setup and Run

Use Python 3.10 or newer. From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`. Visit `http://127.0.0.1:8000/docs` to try the endpoints. `GET /demo-log-errors` writes demo entries to the runtime log file. The prompt-analysis exercise itself requires VS Code with GitHub Copilot Chat; no AI request is made by the Python app.

## Expected Behavior and Limitations

- The sample log contains 3 `DatabaseConnectionError`, 2 `ValueError`, 2 `TimeoutError`, 1 `KeyError`, and 1 `ZeroDivisionError` entries.
- The sample service uses in-memory employee dictionaries and intentionally generated log messages; it is not connected to a real employee database or payment service.
- `main.py` creates the `logs/` directory and opens the runtime log on import/run. Running the app can therefore change the runtime log file; the seeded root-level sample remains the prompt source.
- There are no automated tests or production monitoring integrations.

## What to Study Next

Practice writing a count query or small parser that independently verifies error types and timestamps. Keep raw facts, inferred causes, and recommended actions in separate columns.