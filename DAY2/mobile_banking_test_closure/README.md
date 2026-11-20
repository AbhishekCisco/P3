# Mobile Banking Money Transfer Test Closure

## Overview

This folder is a test-cycle reporting exercise for a fictional mobile-banking money-transfer flow. It contains a static test-results dataset, a written closure report, and a few small Python functions whose earlier bugs have been corrected. It does not contain a banking application or an automated test harness.

## Learning Objectives

- Summarize test execution with clear pass, fail, and blocked counts.
- Calculate pass rate using an explicitly stated denominator.
- Connect failed test cases to defects, severity, risk, and release decisions.
- Identify when blocked tests and unresolved defects prevent a release recommendation.

## Topics Covered

- **Test-cycle metrics:** 9 of 14 executed cases passed (64.3%); one additional case is blocked and excluded from the executed-test pass-rate denominator.
- **Defect triage:** the report relates five failed cases to authentication, reliability, UI, validation, and performance issues.
- **Release readiness:** the report recommends no release because a critical OTP issue remains and the pass rate is below its 95% exit criterion.
- **Basic Python debugging:** `buggy_code.py` contains corrected greeting, integer-input, and age-threshold examples.

## Project Structure

```text
mobile_banking_test_closure/
├── buggy_code.py          # Small corrected Python examples
├── test_closure_report.md # Metrics, defects, risks, and release recommendation
├── test_result.csv        # 15 recorded money-transfer test cases
└── README.md
```

## How the Files Work Together

`test_result.csv` records the execution outcome, module, priority, defect, timing, and notes for each test case. `test_closure_report.md` summarizes those results and explains the open risks and release decision. `buggy_code.py` is a separate coding exercise; it does not calculate the report metrics or connect to a banking system.

The Python examples are `greet(name)`, `add_numbers()` (which converts console input to integers before addition), and `is_eligible_for_discount(age)` (eligible at age 60 or older).

## Setup and Use

No package installation is required. Review the Markdown report and CSV in an editor or spreadsheet program. To try the small Python examples, run `python buggy_code.py`; the number-input example waits for two values in the terminal.

## Current Findings and Limitations

- The report records 15 cases: 9 passed, 5 failed, and 1 blocked. Its 64.3% pass rate is `9 / 14`; blocked tests are not counted as executed.
- TC13 (transfer history update) remains blocked until the retry/duplicate-debit issue is fixed. The report's release recommendation is **Do not release**.
- The CSV and Markdown report are manually maintained artifacts; there is no script that recalculates metrics or checks that they remain consistent.
- No automated tests are included for `buggy_code.py`, and the functions are not connected to a mobile app or payment service.

## What to Study Next

Reconcile each report number against the CSV, distinguish severity from priority, and identify which failed cases need retesting after a fix. Then add a small validation script or tests that detect inconsistencies without treating blocked cases as passes.