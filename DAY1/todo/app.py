"""A small Flask application for managing a task list."""

from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "development-only-change-me"

PRIORITIES = ("High", "Medium", "Low")
CATEGORIES = ("Work", "Personal", "Health")

tasks = []


@app.template_filter("display_date")
def display_date(value):
    """Format an ISO date for display.

    Args:
        value: Date string in ISO 8601 format.

    Returns:
        The date formatted as an abbreviated month, day, and year.
    """
    return date.fromisoformat(value).strftime("%b %d, %Y")


@app.get("/")
def index():
    """Render the task list, ordered by due date.

    Returns:
        The rendered index page.
    """
    # Keep original indexes so delete links still refer to the underlying list.
    sorted_tasks = sorted(enumerate(tasks), key=lambda item: item[1]["due_date"])
    return render_template(
        "index.html",
        tasks=sorted_tasks,
        priorities=PRIORITIES,
        categories=CATEGORIES,
    )


@app.post("/tasks")
def add_task():
    """Validate and add a task submitted through the task form.

    Returns:
        A redirect to the index page after processing the submission.
    """
    task = request.form.get("task", "").strip()
    priority = request.form.get("priority", "")
    category = request.form.get("category", "")
    due_date = request.form.get("due_date", "")

    if not task:
        flash("Enter a task name.", "error")
    elif len(task) > 160:
        flash("Task names must be 160 characters or fewer.", "error")
    elif priority not in PRIORITIES:
        flash("Choose a valid priority.", "error")
    elif category not in CATEGORIES:
        flash("Choose a valid category.", "error")
    else:
        try:
            due_date = date.fromisoformat(due_date).isoformat()
        except ValueError:
            flash("Choose a valid due date.", "error")
        else:
            tasks.append(
                {
                    "task": task,
                    "priority": priority,
                    "category": category,
                    "due_date": due_date,
                }
            )
            flash("Task added to your list.", "success")
    return redirect(url_for("index"))


@app.post("/tasks/<int:task_index>/delete")
def delete_task(task_index):
    """Delete a task by its index in the task list.

    Args:
        task_index: Index of the task to delete.

    Returns:
        A redirect to the index page after processing the request.
    """
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
        flash("Task deleted.", "success")
    else:
        flash("That task could not be found.", "error")
    return redirect(url_for("index"))

def count_tasks_by_priority(tasks, priority):
    count = 0
    for task in tasks:
        if task['priority'] == priority:
            count += 1
    return count



if __name__ == "__main__":
    app.run(debug=True)
