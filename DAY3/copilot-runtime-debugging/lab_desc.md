# Resolving Runtime Errors Using GitHub Copilot Chat with Python FastAPI

**Practical Lab**

*Beginner to Intermediate*

## 1. Lab objective

In this exercise, you will develop a Python FastAPI application containing three intentional runtime errors:

- TypeError – Incorrect data type passed to a function.
- KeyError – Accessing a dictionary key that does not exist.
- ZeroDivisionError – Dividing a number by zero.

You will use GitHub Copilot Chat in VS Code to:

- Reproduce each runtime error.
- Understand the root cause.
- Write structured debugging prompts.
- Ask Copilot to explain before fixing the code.
- Apply the recommended fixes.
- Validate the fixes using Pytest and FastAPI TestClient.
## 2. Project structure

Create the following project using VS Code.

```text
copilot-runtime-debugging/
│
├── main.py
├── requirements.txt
│
└── tests/
    └── test_main.py
```
## 3. Environment setup

### Step 1: Create a virtual environment

Open the VS Code terminal.

For Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Create requirements.txt

Add the following dependencies:

```text
fastapi
uvicorn
pytest
httpx
```
Install the libraries:

```bash
pip install -r requirements.txt
```

## 4. Create FastAPI application with three intentional runtime errors

Create main.py.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="GitHub Copilot Runtime Debugging Lab")


class Employee(BaseModel):
    name: str
    age: int
    salary: float


# ------------------------------------------------
# ERROR 1: TypeError
# ------------------------------------------------

@app.get("/employee/bonus")
def calculate_bonus():
    salary = "50000"

    # Intentional error:
    # String multiplied by float
    bonus = salary * 0.10

    return {"bonus": bonus}


# ------------------------------------------------
# ERROR 2: KeyError
# ------------------------------------------------

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):

    employees = {
        101: {"name": "Rahul", "department": "IT"},
        102: {"name": "Priya", "department": "HR"}
    }

    # Intentional error:
    # Employee ID 999 does not exist
    employee = employees[employee_id]

    return employee


# ------------------------------------------------
# ERROR 3: ZeroDivisionError
# ------------------------------------------------

@app.get("/employee/average-salary")
def calculate_average_salary():

    total_salary = 150000
    employee_count = 0

    # Intentional error:
    # Dividing by zero
    average = total_salary / employee_count

    return {"average_salary": average}


@app.get("/")
def home():
    return {"message": "Runtime Debugging Lab"}
```

## 5. Start the FastAPI application

Run:

```bash
uvicorn main:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

Open Swagger UI:

[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

You should see three endpoints:
| Endpoint | Purpose |
|---|---|
| `GET /employee/bonus` | Calculate employee bonus |
| `GET /employee/{employee_id}` | Get employee details |
| `GET /employee/average-salary` | Calculate average salary |

## 6. Debugging Exercise 1 – Resolve TypeError

### Step 1: Reproduce the error

Execute:

`GET /employee/bonus`

Expected error:

`TypeError: can't multiply sequence by non-int of type 'float'`

### Step 2: Understand the root cause

The problematic code is:

```python
salary = "50000"
bonus = salary * 0.10
```

The salary is stored as a string rather than a numeric value.
Python cannot multiply a string by a floating-point number.

### Step 3: Ask GitHub Copilot Chat

Open Copilot Chat in VS Code and paste this prompt:

#### Copilot debugging prompt 1

**Error:** `TypeError`

```text
You are an expert Python and FastAPI developer.
I am getting the following runtime error in my FastAPI application:
TypeError: can't multiply sequence by non-int of type 'float'
Here is my code:
salary = "50000"
bonus = salary * 0.10
Please perform the following tasks:
Explain the root cause of the error.
Identify the incorrect statement.
Explain why Python throws this exception.
Suggest the minimum code change required to fix it.
Provide the corrected code.
Suggest a unit test to validate the fix.
Do not modify the code until you explain the root cause.
```
**Copy prompt**

### Step 4: Apply the fix

Corrected code:

```python
@app.get("/employee/bonus")
def calculate_bonus():

    salary = 50000.0

    bonus = salary * 0.10

    return {"bonus": bonus}
```

### Step 5: Validate

Execute:

[`http://127.0.0.1:8000/employee/bonus`](http://127.0.0.1:8000/employee/bonus)

Expected response:

```json
{
  "bonus": 5000.0
}
```

**TypeError resolved.**

## 7. Debugging Exercise 2 – Resolve KeyError

### Step 1: Reproduce the error

Execute:

`GET /employee/999`

Expected error:

`KeyError: 999`

### Step 2: Understand the root cause

Problematic code:

```python
employee = employees[employee_id]
```

The dictionary contains only employee IDs 101 and 102.
When you request employee ID 999, Python cannot find that dictionary key and throws a KeyError.

### Step 3: Ask GitHub Copilot Chat

#### Copilot debugging prompt 2

**Error:** `KeyError`

```text
I am developing a FastAPI employee management application.
I am getting the following runtime error:
KeyError: 999
Here is my code:
employees = {
    101: {"name": "Rahul", "department": "IT"},
    102: {"name": "Priya", "department": "HR"}
}

employee = employees[employee_id]
Please:
Explain the root cause.
Identify why employee ID 999 causes an exception.
Explain the difference between dictionary indexing and the get() method.
Suggest a safe solution using FastAPI HTTPException.
Return HTTP 404 when the employee does not exist.
Provide a test case for both existing and missing employee IDs.
Explain before modifying the code.
```
**Copy prompt**

### Step 4: Apply the fix

Corrected code:

```python
@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    employees = {
        101: {"name": "Rahul", "department": "IT"},
        102: {"name": "Priya", "department": "HR"}
    }
    employee = employees.get(employee_id)
    if employee is None:
        raise HTTPException(
            status_code=404,
            detail=f"Employee {employee_id} not found"
        )
    return employee
```

### Step 5: Validate

Test existing employee:

[`http://127.0.0.1:8000/employee/101`](http://127.0.0.1:8000/employee/101)

Expected response:

```json
{
  "name": "Rahul",
  "department": "IT"
}
```

Test missing employee:

[`http://127.0.0.1:8000/employee/999`](http://127.0.0.1:8000/employee/999)

Expected response:

```json
{
  "detail": "Employee 999 not found"
}
```

HTTP status code:

`404 Not Found`

**KeyError resolved.**

## 8. Debugging Exercise 3 – Resolve ZeroDivisionError

### Step 1: Reproduce the error

Execute:

`GET /employee/average-salary`

Expected error:

`ZeroDivisionError: division by zero`

### Step 2: Understand the root cause

Problematic code:

```python
total_salary = 150000
employee_count = 0

average = total_salary / employee_count
```

The denominator is zero.
Python does not allow division by zero.

### Step 3: Ask GitHub Copilot Chat

#### Copilot debugging prompt 3

**Error:** `ZeroDivisionError`

```text
I am developing an employee salary API using Python FastAPI.
I am getting this runtime error:
ZeroDivisionError: division by zero
Here is my code:
total_salary = 150000
employee_count = 0
average = total_salary / employee_count
Please:
Explain the root cause.
Identify why division by zero is invalid.
Suggest a defensive programming solution.
Explain how to handle zero employees.
Return a meaningful HTTP 400 error when employee count is zero.
Provide unit tests for zero and non-zero employee counts.
First explain the error, then suggest the fix. Do not directly modify the code.
```
**Copy prompt**

### Step 4: Apply the fix

Corrected code:

```python
@app.get("/employee/average-salary")
def calculate_average_salary():

    total_salary = 150000
    employee_count = 3

    if employee_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot calculate average salary: no employees found"
        )

    average = total_salary / employee_count

    return {"average_salary": average}
```

For proper testing, we can make this function accept the employee count as a query parameter.

Improved implementation:

```python
@app.get("/employee/average-salary")
def calculate_average_salary(
    total_salary: float = 150000,
    employee_count: int = 3
):

    if employee_count <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee count must be greater than zero"
        )

    average = total_salary / employee_count

    return {"average_salary": average}
```

### Step 5: Validate

Test successful calculation:

[`http://127.0.0.1:8000/employee/average-salary?total_salary=150000&employee_count=3`](http://127.0.0.1:8000/employee/average-salary?total_salary=150000&employee_count=3)

Expected response:

```json
{
  "average_salary": 50000.0
}
```

Test zero employees:

[`http://127.0.0.1:8000/employee/average-salary?total_salary=150000&employee_count=0`](http://127.0.0.1:8000/employee/average-salary?total_salary=150000&employee_count=0)

Expected response:

```json
{
  "detail": "Employee count must be greater than zero"
}
```

**ZeroDivisionError resolved.**

## 9. Validate all fixes using Pytest

Now let's automate the testing process.

Create tests/test_main.py.

```python
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
# Test 1: TypeError fix
def test_calculate_bonus():
    response = client.get("/employee/bonus")
    assert response.status_code == 200
    assert response.json()["bonus"] == 5000.0


# Test 2: KeyError fix - Existing employee
def test_get_existing_employee():
    response = client.get("/employee/101")
    assert response.status_code == 200
    assert response.json()["name"] == "Rahul"
# Test 3: KeyError fix - Missing employee
def test_get_missing_employee():

    response = client.get("/employee/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee 999 not found"


# Test 4: ZeroDivisionError fix - Valid calculation
def test_average_salary():

    response = client.get(
        "/employee/average-salary",
        params={
            "total_salary": 150000,
            "employee_count": 3
        }
    )

    assert response.status_code == 200
    assert response.json()["average_salary"] == 50000.0


# Test 5: ZeroDivisionError fix - Zero employees
def test_zero_employee_count():

    response = client.get(
        "/employee/average-salary",
        params={
            "total_salary": 150000,
            "employee_count": 0
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Employee count must be greater than zero"
    )

```

Run the test cases

Execute this command from the project root:

```bash
pytest -v
```

### Pytest execution results

Expected output:

```text
5 PASSED
test_calculate_bonus PASSED
test_get_existing_employee PASSED
test_get_missing_employee PASSED
test_average_salary PASSED
test_zero_employee_count PASSED
5 / 5
All test cases passed
```

Expected result after applying all three fixes.

## 10. GitHub Copilot Chat – Final validation prompt

After fixing all three errors, ask Copilot to review the complete application.

#### Final Copilot review prompt
```text
Review my complete Python FastAPI application and its Pytest test cases.
Three runtime errors were originally introduced:
TypeError
KeyError
ZeroDivisionError
Perform the following tasks:
Verify that all three runtime errors have been resolved.
Review the exception-handling logic.
Check whether appropriate HTTP status codes are returned.
Review the test coverage.
Identify any remaining potential runtime issues.
Suggest improvements following Python and FastAPI best practices.
Do not change any code without explaining the proposed changes first.
```
**Copy final prompt**

## 11. End-to-end lab execution flow

### Runtime debugging workflow

1. **Create the FastAPI application:** Introduce three intentional runtime errors.
2. **Execute APIs:** Reproduce TypeError, KeyError and ZeroDivisionError.
3. **Open GitHub Copilot Chat:** Provide structured debugging prompts.
4. **Understand the root cause:** Ask Copilot to explain the exception before suggesting changes.
5. **Fix the code:** Apply and review the recommended changes.
6. **Execute Pytest:** Validate successful and failure scenarios.
7. **Final code review:** Ask Copilot to identify remaining issues.

### Additional challenge

- ValueError: Pass invalid employee salary values.
- AttributeError: Access a non-existent object attribute.
- IndexError: Access an invalid list index.
- ValidationError: Send an invalid employee JSON payload.
For each scenario, reproduce the error, ask Copilot to explain the root cause, implement a fix, and write a test. 
# Lab-2 Extracting Error Patterns from Application Logs Using AI

## 1. Objective

In this exercise, we will use GitHub Copilot Chat in VS Code to analyze application logs generated by a Python FastAPI application.
They will learn how to use AI to:

- Read and summarize application logs.
- Identify recurring errors and exceptions.
- Group errors by type and count their occurrences.
- Investigate error patterns and potential root causes.
- Validate AI-generated findings against actual log entries.

> **Important learning principle:** GitHub Copilot should assist with log analysis, but the developer must validate every finding against the original log data.

## 2. Demo architecture

1. **Python FastAPI application** — Generates application events and errors.
2. **Application log file** — `application.log`.
3. **GitHub Copilot Chat** — Summarize → Group → Count → Investigate.
4. **Developer validation** — Compare AI findings with raw log lines.

## 3. Create the project structure

Create a project named ai-log-analysis.

```text
ai-log-analysis/
│
├── main.py
├── requirements.txt
├── application.log
│
└── logs/
    └── .gitkeep
```
## 4. Environment setup

Create and activate a virtual environment.

Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
Create requirements.txt:
```text
fastapi
uvicorn
```
Install dependencies:

```bash
pip install -r requirements.txt
```

## 5. Set up the application log

For this demonstration, we will use a sample FastAPI application log containing different types of errors.
Create a file named application.log and add the following entries.

```log
2026-11-17 09:00:01 INFO Application started successfully
2026-11-17 09:01:12 INFO Employee API request received
2026-11-17 09:02:15 ERROR DatabaseConnectionError: Unable to connect to database
2026-11-17 09:02:20 ERROR DatabaseConnectionError: Unable to connect to database
2026-11-17 09:03:05 WARNING Slow database response: 8 seconds
2026-11-17 09:04:10 ERROR ValueError: Invalid employee salary value
2026-11-17 09:04:45 ERROR ValueError: Invalid employee salary value
2026-11-17 09:05:12 INFO Employee record created successfully
2026-11-17 09:06:30 ERROR TimeoutError: External payment API request timed out
2026-11-17 09:06:55 ERROR TimeoutError: External payment API request timed out
2026-11-17 09:07:10 WARNING Payment API response delayed
2026-11-17 09:08:22 ERROR DatabaseConnectionError: Unable to connect to database
2026-11-17 09:09:15 INFO Employee details fetched successfully
2026-11-17 09:10:30 ERROR KeyError: Employee ID not found
2026-11-17 09:11:00 INFO Application health check successful
2026-11-17 09:12:10 ERROR ZeroDivisionError: Division by zero
2026-11-17 09:13:45 WARNING High API response time detected
2026-11-17 09:14:20 INFO Application request completed
```

We have deliberately included:

- **INFO** messages — Normal application activity.
- **WARNING** messages — Potential performance issues.
- **ERROR** messages — Actual application failures.

This is the raw source file that Copilot will analyze.

## 6. Activity 1 – Summarize the log using Copilot Ask mode

### Step 1: Open GitHub Copilot Chat

1. Open VS Code.
2. Open the `ai-log-analysis` project.
3. Open GitHub Copilot Chat.
4. Select **Ask** mode.

#### Prompt 1 – Log summarization

```text
Ask mode
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

**Copy prompt**

Expected AI response

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

## 7. Activity 2 – Group and count errors using a structured prompt

Now we will ask Copilot to identify recurring error patterns.

### Step 1: Enter the structured prompt

#### Prompt 2 – Error classification

**Structured prompt**

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
**Copy prompt**

### Step 2: Expected AI output

The expected classification is:

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
