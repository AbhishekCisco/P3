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
    """Return a 10% bonus after converting the salary string to a number.

    Multiplying a string by a float raised TypeError because string
    repetition requires an integer. Converting to float enables arithmetic.
    """
    salary = "50000"
    bonus = float(salary) * 0.10

    return {"bonus": bonus}


# ------------------------------------------------
# ERROR 3: ZeroDivisionError
# ------------------------------------------------

@app.get("/employee/average-salary")
def calculate_average_salary(
    total_salary: float = 150000,
    employee_count: int = 8,
):
    """Return the average salary for a positive employee count.

    A zero count raised ZeroDivisionError because the average is undefined.
    Reject non-positive counts with HTTP 400 before dividing. Register this
    static route before the employee ID route so it isn't mistaken for an ID.
    """
    if employee_count <= 0:
        raise HTTPException(
            status_code=400,
            detail="Employee count must be greater than zero",
        )

    return {"average_salary": total_salary / employee_count}


# ------------------------------------------------
# ERROR 2: KeyError
# ------------------------------------------------

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    """Return an employee by ID or respond with HTTP 404.

    Direct dictionary indexing raised KeyError for missing IDs. Using get()
    returns None instead, so the endpoint can report which ID was not found.
    """
    employees = {
        101: {"name": "Rahul", "department": "IT"},
        102: {"name": "Priya", "department": "HR"}
    }

    employee = employees.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    return employee


@app.get("/")
def home():
    return {"message": "Runtime Debugging Lab"}
