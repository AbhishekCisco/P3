# Python Runtime Error Debugging Exercise

## Overview

This project is a small, non-web exercise about explaining and fixing a `TypeError`, `KeyError`, and `ZeroDivisionError`. The functions in `buggy_functions.py` already contain the corrected behavior, and `test_fixed_functions.py` checks the expected results. The lab document walks through the original failures and a Copilot-assisted debugging process.

## Learning Objectives

- Convert values to the types needed for an operation.
- Handle dictionary lookups when a key may be missing.
- Define useful behavior for an empty list rather than dividing by zero.
- Write regression tests that cover the original failing cases.

## Topics Covered

- **String formatting:** the alert count is converted to text before joining the message.
- **Safe lookup:** `dict.get()` supplies the `Unassigned` fallback for an unknown owner.
- **Empty-input handling:** an empty response-time list returns `0.0`; non-empty input returns its arithmetic mean.
- **Test-driven validation:** five pytest tests cover normal and edge-case results.

## Project Structure

```text
debug_lab/
├── buggy_functions.py       # Functions after the fixes
├── lab_desc.md              # Guided prompts and original bug scenarios
├── test_fixed_functions.py  # Five regression tests
└── README.md
```

## How the Files Work Together

`buggy_functions.py` defines `format_alert_summary()`, `get_alert_owner()`, and `average_response_time()`. `test_fixed_functions.py` imports those functions and verifies ordinary inputs plus missing-owner and empty-list cases. `lab_desc.md` provides the learning workflow and the commands/prompts for reproducing and discussing the earlier failures.

## Setup and Run

Use Python 3.10 or newer. There is no dependency file; install pytest in a virtual environment and run the test from this folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`.

## Current Status and Limitations

- The guide contains an older setup fragment followed by a fuller formatted version; the current source and test are the authoritative implementation.
- The exercise is a set of pure Python functions, not a running service, and has no packaging or dependency configuration.
- The test file uses no fixtures or external services.

## What to Study Next

Add tests for invalid alert structures, non-numeric response times, and the behavior expected when an owner key itself is missing. Decide those contracts explicitly before implementing them.