# Evidence-Based Log Analysis Lab

## Overview

This is a prompt-writing and log-reading exercise built around a fixed synthetic log excerpt. It teaches learners to ask an AI assistant for summaries and grouped error counts, then verify every count against the source entries. There is no application or analysis script in this folder.

## Learning Objectives

- Summarize a chronological log without losing important events.
- Group repeated failures and warnings while preserving timestamps and affected IDs.
- Separate facts in the log from possible root causes.
- Independently verify AI-produced counts with fixed-string searches.

## Topics Covered

- **Log levels and patterns:** the sample includes INFO, WARN, HTTP 404, and repeated HTTP 500/`AttributeError` entries.
- **Prompt structure:** the guide asks for specific tables and evidence rather than open-ended speculation.
- **Operational reasoning:** retry messages have no recorded outcomes, so they do not prove the retry succeeded.
- **Manual verification:** expected pattern counts are five attribute errors, one 404, and two database-pool warnings.

## Project Structure

```text
log_analysis_lab/
├── app.log     # Fixed log sample for the exercise
├── lab_desc.md # Copilot prompts, expected findings, and verification steps
└── README.md
```

## How the Files Work Together

`lab_desc.md` provides a sequence of Ask-mode prompts and expected findings. Each prompt analyzes `app.log`; the learner then checks exact strings, timestamps, retry messages, and affected alert IDs against that same file. Possible technical explanations are explicitly hypotheses unless supported by additional evidence.

## Setup and Use

No Python dependencies are required. Open this folder in VS Code with GitHub Copilot Chat available, read `lab_desc.md`, and run the prompts against `app.log`. The guide also includes PowerShell and Linux/macOS fixed-string count examples.

## Current Status and Limitations

- The log is synthetic training data, not a live service log.
- The records establish timing and repeated symptoms, but they do not prove why the `AttributeError` occurred or what happened after each retry.
- There is no automated validator or test suite; manual comparison with the raw log is part of the exercise.

## What to Study Next

Write a small parser that reports counts and time ranges, then compare its output with the AI summary. Keep the original raw message available so grouping does not hide meaningful differences.