# AI Log Analysis with GitHub Copilot

## Activity 1 – Summarize the log using Copilot Ask mode

### Step 1: Open GitHub Copilot Chat

1. Open VS Code.
2. Open the `ai-log-analysis` project.
3. Open GitHub Copilot Chat.
4. Select **Ask** mode.

### Prompt 1 – Log summarization

```text
#file:application.log
Analyze the attached application.log file.
Act as an experienced application support engineer.
Perform the following tasks:
Summarize the overall application activity.
Identify the total number of log entries.
Count INFO, WARNING and ERROR entries.
Identify the different error types.
Highlight the most important application issues.
Provide a short operational health summary.
Do not modify the log file or generate code. Base your analysis only on the supplied log entries.
```

### Expected AI response

Copilot should produce a summary similar to this:

| Log level | Expected count |
|---|---:|
| INFO | 6 |
| WARNING | 3 |
| ERROR | 9 |
| **Total** | **18** |

Key observations:

- Database connectivity failures occurred repeatedly.
- Invalid employee salary values were reported.
- External payment API requests timed out.
- Employee lookup and salary calculation errors occurred.
- The application started and completed some operations successfully.

## Activity 2 – Group and count errors using a structured prompt

Now ask Copilot to identify recurring error patterns.

### Step 1: Enter the structured prompt

### Prompt 2 – Error classification

```text
Analyze application.log and extract recurring error patterns.
Group the errors based on their exception type.
For each error group, provide:
Error type.
Total occurrences.
Example error message.
First occurrence timestamp.
Last occurrence timestamp.
Possible root cause.
Suggested corrective action.
Present the results in a structured Markdown table.
Separate actual errors from warnings.
Do not assume that repeated messages always have the same root cause. Clearly distinguish observed facts from hypotheses.
```

### Step 2: Expected AI output

| Error type | Occurrences | First occurrence | Last occurrence |
|---|---:|---|---|
| `DatabaseConnectionError` | 3 | 09:02:15 | 09:08:22 |
| `ValueError` | 2 | 09:04:10 | 09:04:45 |
| `TimeoutError` | 2 | 09:06:30 | 09:06:55 |
| `KeyError` | 1 | 09:10:30 | 09:10:30 |
| `ZeroDivisionError` | 1 | 09:12:10 | 09:12:10 |
| **Total** | **9** | | |

Observations:

- Database connectivity is the most frequently occurring error.
- `ValueError` and `TimeoutError` have two occurrences each.
- `KeyError` and `ZeroDivisionError` appear once each.
- Database connectivity and payment API timeouts deserve further investigation.
- Frequency alone does not establish business impact or root cause.

## Activity 3 – Query the error pattern in more detail

### Scenario A: Investigate `DatabaseConnectionError`

Ask Copilot:

### Prompt 3 – Deep error investigation

```text
In application.log, DatabaseConnectionError occurs multiple times.
Investigate this error pattern in detail.
Please answer:
How many times does it occur?
At what timestamps does it occur?
What is the time difference between consecutive occurrences?
Does the log indicate a continuous or intermittent failure?
What are the possible technical reasons?
What additional logs or metrics should be checked?
Suggest preventive and corrective actions.
Clearly separate facts available in the log from possible explanations.
```

Expected findings:

- Occurrences: 3.
- Timestamps: 09:02:15, 09:02:20 and 09:08:22.
- The first two failures are only 5 seconds apart.
- The third failure occurs 6 minutes and 7 seconds after the first.
- Possible causes to investigate:
  - Database server availability.
  - Connection pool exhaustion.
  - Network connectivity.
  - Database authentication or configuration.
  - Database resource limitations.
- These are hypotheses, not confirmed causes from the supplied log.

### Scenario B: Investigate `TimeoutError`

### Prompt 4 – Payment API timeout analysis

```text
Analyze all TimeoutError entries in application.log.
Identify:
Total occurrences.
Failure timestamps.
Whether failures occurred close together.
Potential impact on payment processing.
Possible reasons for API timeouts.
Recommended timeout, retry and monitoring strategies.
Explain how to distinguish a temporary external API issue from a persistent integration issue.
Do not assume that a payment failed just because the API timed out. Explain how payment status should be verified.
```

Expected findings:

- Two timeout errors.
- Both occur within 25 seconds.
- Both relate to the external payment API.
- Investigate API latency, connectivity, timeout configuration and retry handling.
- Verify transaction status before retrying a payment to avoid duplicate transactions.

## Activity 4 – Validate AI findings against raw log entries

This is the most important part of the exercise. Do not blindly accept Copilot's summary. Verify the error counts and timestamps against the original `application.log`.

### Step 1: Ask Copilot for evidence

### Prompt 5 – Evidence-based validation

```text
Validate your previous error analysis against the original application.log.
For each identified error:
Provide the exact raw log entry.
Mention its line number in the log file.
Verify the total occurrence count.
Verify the first and last timestamps.
Identify any missing or incorrectly classified entries.
Provide a final table with:
Error Type | AI Count | Verified Count | Validation Status
Do not create or assume any log entries. Use only the original log file as evidence.
```

### Step 2: Verify manually using terminal commands

Participants can independently validate the counts. For example, count database errors in Windows PowerShell using:

```powershell
Select-String -Path .\application.log -Pattern 'DatabaseConnectionError' | Measure-Object -Line
```

## Demo application source

The following FastAPI application generates representative log entries for the exercise:

```python
from datetime import datetime
from pathlib import Path
import logging

from fastapi import FastAPI, HTTPException


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


# Log to both the terminal and logs/application.log.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "application.log", encoding="utf-8"),
    ],
)


logger = logging.getLogger("ai_log_analysis")
app = FastAPI(title="AI Log Analysis Demo", version="1.0.0")


@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "AI Log Analysis Demo is running"}


@app.get("/health")
def health():
    logger.info("Health check successful")
    return {"status": "healthy"}


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    # Demo data only; replace with a database in a real application.
    employees = {
        101: {"name": "Rahul", "department": "IT"},
        102: {"name": "Priya", "department": "HR"},
    }

    employee = employees.get(employee_id)
    if employee is None:
        logger.error("EmployeeNotFound: employee_id=%s", employee_id)
        raise HTTPException(status_code=404, detail="Employee not found")

    logger.info("Employee %s fetched successfully", employee_id)
    return employee


@app.get("/employees/{employee_id}/bonus")
def calculate_bonus(employee_id: int):
    employees = {
        101: {"name": "Rahul", "salary": 50000.0},
        102: {"name": "Priya", "salary": 60000.0},
    }

    employee = employees.get(employee_id)
    if employee is None:
        logger.error("EmployeeNotFound: employee_id=%s", employee_id)
        raise HTTPException(status_code=404, detail="Employee not found")

    bonus = employee["salary"] * 0.10
    logger.info("Bonus calculated for employee_id=%s", employee_id)
    return {"employee_id": employee_id, "bonus": bonus}


@app.get("/demo-log-errors")
def generate_demo_errors():
    """Write representative demo errors to the runtime log.

    This endpoint deliberately logs error patterns for the Copilot exercise.
    It does not deliberately crash the API.
    """
    logger.error("DatabaseConnectionError: Unable to connect to database")
    logger.error("DatabaseConnectionError: Unable to connect to database")
    logger.warning("Slow database response: 8 seconds")
    logger.error("ValueError: Invalid employee salary value")
    logger.error("ValueError: Invalid employee salary value")
    logger.error("TimeoutError: External payment API request timed out")
    logger.error("TimeoutError: External payment API request timed out")
    logger.warning("Payment API response delayed")
    logger.error("DatabaseConnectionError: Unable to connect to database")
    logger.error("KeyError: Employee ID not found")
    logger.error("ZeroDivisionError: Division by zero")
    logger.warning("High API response time detected")

    logger.info("Demo error patterns generated")
    return {
        "message": "Demo log patterns written",
        "log_file": str(LOG_DIR / "application.log"),
    }
```