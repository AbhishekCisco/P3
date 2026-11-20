# Worklist

A single-page, business-oriented to-do web application built with Python Flask.
Add tasks, organize them by priority and category, and view upcoming work in a
table sorted by due date, earliest first.

## Features

- Add a task with a name (up to 160 characters), priority, category, and due date.
- Choose a priority: **High**, **Medium**, or **Low**.
- Choose a category: **Work**, **Personal**, or **Health**.
- All task fields are required and validated by the server.
- View tasks in a due-date-sorted table with color-coded labels.
- Delete tasks using the button on each row.
- Use a responsive interface with CSS included in the HTML template.

Tasks are stored in an **in-memory Python list**, not a database. Each task is a
dictionary with the keys `task`, `priority`, `category`, and `due_date`. Tasks are
shared by users of the same running process and are lost when the app stops,
restarts, or reloads after a code change.

## Requirements

- Python 3.9 or newer (Python 3.12 is recommended).
- `pip` and Python's `venv` module.

The Flask dependency is declared in [requirements.txt](requirements.txt).

## Setup

Open a terminal in this project's folder.

### Linux or macOS

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

Create and activate a virtual environment:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If a virtual environment named `venv` already exists, skip the creation command
and activate it using the command for your operating system.

### Install dependencies

With the virtual environment activated, run:

```bash
python -m pip install -r requirements.txt
```

## Run the app

From the project folder, with the virtual environment activated:

```bash
python app.py
```

Open **http://127.0.0.1:5000/** in your browser.

1. Enter a task name.
2. Select its priority and category.
3. Pick a due date and click **Add task**.
4. Click **Delete** on a row to remove that task.

Press `Ctrl+C` in the terminal to stop the server. Run `deactivate` when you are
finished using the virtual environment.

## Project structure

```text
.
├── app.py                # Flask routes, validation, and in-memory task list
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Task form, table, and inline CSS
└── README.md
```

## Development notes

- Running `python app.py` enables Flask's debug mode and automatic reloader.
  The development server and the placeholder secret key in
  [app.py](app.py) are intended for local development, not production use.
- There are no user accounts or persistent storage.
- Delete actions use positions in the in-memory list. Refresh other open tabs
  after deleting a task to avoid acting on outdated row positions.
- `count_tasks_by_priority()` is defined in `app.py` but is not currently used
  by a route or template.
- There is no automated test suite. Server-side validation is implemented in
  the add-task route, while browser `required` attributes provide an additional
  user-interface check.

## Learning Objectives

- Build a small web workflow with Flask route functions and Jinja templates.
- Handle form submissions, validate values on the server, and use the
  post/redirect/get pattern.
- Render sorted in-memory data and display categorized status messages.
- Understand the tradeoff between simple process-local state and persistent
  database storage.

## Topics Covered

- **Routing and forms:** `app.py` serves the list and accepts add/delete POSTs.
- **Validation:** task length, priority, category, and ISO due-date values are
  checked before data is appended.
- **Templating:** `templates/index.html` renders the form, task table, empty
  state, flash messages, and responsive inline CSS.
- **Transient state:** an in-memory list makes the example easy to follow but
  loses all tasks on process restart and is not shared across worker processes.
