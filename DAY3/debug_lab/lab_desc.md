Lesson 03 Demo 03
 
Resolving Runtime Errors Using GitHub Copilot Chat: Explain and Fix
Objective: To resolve three runtime errors with GitHub Copilot Chat by reproducing each error, writing a structured debugging prompt, asking Copilot to explain the root cause before fixing it, and validating every fix with tests.
Prerequisites:
•  Visual Studio Code with GitHub Copilot signed in (Coding module, Demo 01)
•  Python 3.10 or later installed
 
Steps to be followed:
1.  Set up the code with three runtime errors
2.  Resolve the TypeError
3.  Resolve the KeyError
4.  Resolve the ZeroDivisionError
5.  Validate all the fixes with tests
 
The debugging workflow used for each error: 1. Reproduce the error.  2. Write a structured debugging prompt in Ask mode: the exact error, the input that causes it, the expected behavior, and the code (#file).  3. Ask Copilot to explain the root cause before changing anything.  4. Fix the code with inline chat (Ctrl+I) and review the change before you click Keep.  5. Rerun the failing call to confirm the fix.
Step 1: Set up the code with three runtime errors
1.      Open Visual Studio Code. Select File > Open Folder, create a new folder named debug_lab, and open it
2.     Press Ctrl+Alt+I to open the Copilot Chat view, select Agent mode, and enter the prompt "Create a Python virtual environment named .venv in this folder." Review the command that Copilot proposes, and then click Allow.
3.     Select Terminal > New Terminal and run the following commands to activate the virtual environment and install pytest:
PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install pytest

 
4.  Create a file named buggy_functions.py with the following code, and save it. Each function has one intentional runtime error:
Python (buggy_functions.py)
def format_alert_summary(alert_count, severity):
	return "There are " + alert_count + " " + severity + " alerts active."
 
 
def get_alert_owner(alert, team_directory):
	return team_directory[alert["owner"]]
# Lesson 03, Demo 03

## Resolving Runtime Errors with GitHub Copilot Chat: Explain and Fix

**Objective:** Resolve three runtime errors by reproducing each error, writing a structured debugging prompt, asking Copilot to explain the root cause before fixing it, and validating every fix with tests.

**Prerequisites:**

- Visual Studio Code with GitHub Copilot signed in (Coding module, Demo 01)
- Python 3.10 or later

**Steps:**

1. Set up code with three runtime errors.
2. Resolve the `TypeError`.
3. Resolve the `KeyError`.
4. Resolve the `ZeroDivisionError`.
5. Validate all fixes with tests.

For each error, follow this workflow:

1. Reproduce the error.
2. In Ask mode, write a structured debugging prompt that includes the exact error, the input that causes it, the expected behavior, and the code reference (`#file`).
3. Ask Copilot to explain the root cause before changing anything.
4. Use inline chat (`Ctrl+I`) to fix the code, then review the change before clicking **Keep**.
5. Rerun the failing call to confirm the fix.

## Step 1: Set Up the Code

1. Open Visual Studio Code. Select **File > Open Folder**, create a folder named `debug_lab`, and open it.
2. Press `Ctrl+Alt+I` to open Copilot Chat, select **Agent** mode, and enter:

	> Create a Python virtual environment named `.venv` in this folder.

	Review the proposed command, then click **Allow**.

3. Select **Terminal > New Terminal** and run these commands to activate the virtual environment and install pytest:

	```powershell
	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	.\.venv\Scripts\Activate.ps1
	pip install pytest
	```

4. Create and save `buggy_functions.py`. Each function contains one intentional runtime error:

	```python
	def format_alert_summary(alert_count, severity):
		 return "There are " + alert_count + " " + severity + " alerts active."


	def get_alert_owner(alert, team_directory):
		 return team_directory[alert["owner"]]


	def average_response_time(response_times):
		 return sum(response_times) / len(response_times)
	```

## Step 2: Resolve the `TypeError`

1. Reproduce the error by running this command in the terminal:

	```powershell
	python -c "from buggy_functions import format_alert_summary; print(format_alert_summary(3, 'critical'))"
	```

	**Expected result:** The traceback ends with `TypeError: can only concatenate str (not "int") to str`.

2. Press `Ctrl+Alt+I` to open Copilot Chat, select **Ask** mode, and enter this structured debugging prompt:

	**Prompt (Ask mode):**

	```text
	format_alert_summary(3, 'critical') in #file:buggy_functions.py raises TypeError: can only concatenate str (not "int") to str.
	Expected: it should return 'There are 3 critical alerts active.'
	Explain the root cause. Do not change the code yet.
	```

	**Expected result:** Copilot explains that `alert_count` is an integer and the `+` operator cannot concatenate it with a string without converting it first.

	**Copilot response:**

3. In `buggy_functions.py`, select `format_alert_summary()`, press `Ctrl+I`, and enter this prompt:

	**Prompt (inline chat):**

	```text
	Fix the TypeError in this function so that it works when alert_count is an int. Keep the function signature unchanged.
	```

4. Review the fix (for example, `str(alert_count)` or an f-string), click **Keep**, save the file, and rerun the command from Step 2.1.

	**Expected result:** `There are 3 critical alerts active.`

	**Updated code:**

## Step 3: Resolve the `KeyError`

1. Reproduce the error:

	```powershell
	python -c "from buggy_functions import get_alert_owner; print(get_alert_owner({'id': 5, 'owner': 'network-team'}, {'db-team': 'Asha Patel'}))"
	```

	**Expected result:** The traceback ends with `KeyError: 'network-team'`.

2. In Copilot Chat, select **Ask** mode and enter this structured debugging prompt:

	**Prompt (Ask mode):**

	```text
	get_alert_owner() in #file:buggy_functions.py raises KeyError: 'network-team' when the alert's owner team is not in team_directory.
	Expected: it should return 'Unassigned' instead of crashing.
	Explain the root cause. Do not change the code yet.
	```

	**Expected result:** Copilot explains that `team_directory[...]` raises a `KeyError` for a missing key and suggests `dict.get()` with a default value.

	**Copilot response:**

3. Select `get_alert_owner()`, press `Ctrl+I`, and enter this prompt:

	**Prompt (inline chat):**

	```text
	Fix this function so that it returns 'Unassigned' when the owner team is not in team_directory.
	```

4. Review the fix, click **Keep**, save the file, and rerun the command from Step 3.1.

	**Expected result:** `Unassigned`.

## Step 4: Resolve the `ZeroDivisionError`

1. Reproduce the error:

	```powershell
	python -c "from buggy_functions import average_response_time; print(average_response_time([]))"
	```

	**Expected result:** The traceback ends with `ZeroDivisionError: division by zero`.

2. In Copilot Chat, select **Ask** mode and enter this structured debugging prompt:

	**Prompt (Ask mode):**

	```text
	average_response_time([]) in #file:buggy_functions.py raises ZeroDivisionError: division by zero.
	Expected: it should return 0.0 for an empty list.
	Explain the root cause. Do not change the code yet.
	```

	**Expected result:** Copilot explains that `len([])` is `0`, so the function divides by zero.

	**Copilot response:**

3. Select `average_response_time()`, press `Ctrl+I`, and enter this prompt:

	**Prompt (inline chat):**

	```text
	Fix this function so that it returns 0.0 for an empty list instead of raising ZeroDivisionError.
	```

	**Updated code:**

4. Review the fix, click **Keep**, save the file, and rerun the command from Step 4.1.

	**Expected result:** `0.0`.

> **Note:** A vague prompt such as “fix this” often produces a fix that hides the symptom (for example, wrapping the line in a bare `try/except`). Giving Copilot the exact error, the input, and the expected behavior leads to a fix for the root cause.

## Step 5: Validate the Fixes with Tests

1. Create `test_fixed_functions.py` with these tests. They cover normal cases and the original bugs:

	```python
	from buggy_functions import format_alert_summary, get_alert_owner, average_response_time


	def test_format_alert_summary_with_int_count():
		 assert format_alert_summary(3, "critical") == "There are 3 critical alerts active."


	def test_get_alert_owner_known_team():
		 team_directory = {"db-team": "Asha Patel", "api-team": "Jordan Lee"}
		 alert = {"id": 6, "owner": "db-team"}
		 assert get_alert_owner(alert, team_directory) == "Asha Patel"


	def test_get_alert_owner_unknown_team_returns_fallback():
		 """Confirms the original KeyError case no longer crashes."""
		 team_directory = {"db-team": "Asha Patel", "api-team": "Jordan Lee"}
		 alert = {"id": 5, "owner": "network-team"}
		 assert get_alert_owner(alert, team_directory) == "Unassigned"


	def test_average_response_time_normal_list():
		 assert average_response_time([120, 80, 100]) == 100.0


	def test_average_response_time_empty_list_returns_zero():
		 """Confirms the original ZeroDivisionError case no longer crashes."""
		 assert average_response_time([]) == 0.0
	```

2. Run the tests:

	```powershell
	python -m pytest test_fixed_functions.py -v
	```

	**Expected result:** All five tests pass.

## Validation Checklist

| Check | Expected result | Pass / Fail |
| --- | --- | --- |
| Errors reproduced | `TypeError`, `KeyError`, and `ZeroDivisionError` reproduced before any fix | |
| Structured prompts | Each prompt includes the exact error, input, expected behavior, and `#file` | |
| Root causes explained | Copilot explains each cause before any code is changed | |
| Fixes applied | Each failing call returns a value instead of raising an error | |
| Tests | `python -m pytest test_fixed_functions.py -v`: five tests pass | |

By following these steps, you have used GitHub Copilot Chat to explain and fix three runtime errors with structured debugging prompts, then validated every fix with tests.
