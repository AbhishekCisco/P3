# Prompt Engineering Examples

## Overview

This folder is an interactive command-line lab for comparing five prompting patterns through the Groq chat completions API. It belongs to DAY4's prompt-engineering material and makes real network requests rather than simulating model answers.

## Learning Objectives

- Compare zero-shot, few-shot, role-based, and repeated-sample prompts.
- Separate system instructions from a user task.
- Observe how examples and output constraints influence a model response.
- Validate generated calculations and code rather than assuming agreement means correctness.

This project is a small interactive lab for trying five prompt-engineering
patterns with the Groq chat completions API. Run `main.py` and choose an
example from the menu; each selection sends one or more requests to the
configured model and prints its response.

## What the examples demonstrate

| Menu option | Technique | What it does in this project |
| --- | --- | --- |
| 1 | Zero-shot prompting | Requests a Python function to find the largest number in a list without giving examples. |
| 2 | Few-shot prompting | Shows three rating-to-label examples, then asks the model to classify a rating of 10 using the demonstrated pattern. |
| 3 | Chain-of-thought-style prompting | Asks for a concise step-by-step calculation of salary from basic pay, HRA, and bonus. |
| 4 | Role-based prompting | Sets a system message describing a senior Python developer, then asks for a commented Pandas program with specific requirements. |
| 5 | Self-consistency prompting | Makes three separate requests for the same percentage calculation, then asks the model to compare and verify the answers. |

### 1. Zero-shot prompting

Zero-shot means providing the task and desired output without examples. Here,
the prompt asks for code to find the largest number in a list and requests an
explanation. This is a useful baseline when the task is straightforward and
the expected output can be described clearly.

### 2. Few-shot prompting

Few-shot prompting includes examples in the prompt so the model can infer the
desired input-to-output pattern. The script provides three employee-rating
classifications and asks for a classification of rating `10`. The examples
illustrate a pattern; they do not define a complete scoring policy for every
possible rating.

### 3. Chain-of-thought-style prompting

This example asks the model to show a concise calculation before giving the
total salary. For the inputs in the prompt, HRA is 20% of 40,000 and the bonus
is 10% of 40,000. Treat a generated explanation as something to verify, not as
a guarantee that the answer is correct.

### 4. Role-based prompting

This example separates the instructions into two parts:

- The **system message** describes the assistant's role, coding style, and
  explanation style.
- The **user prompt** gives the concrete Pandas task and its requirements.

The role is guidance for the response, not proof of the model's expertise or a
guarantee that the generated program will work without testing.

### 5. Self-consistency prompting

The script sends the same calculation prompt three times, stores the returned
answers, and sends them to a final comparison request. This demonstrates using
multiple generated attempts as a consistency check. It is not a formal voting
algorithm: the attempts may agree and still be wrong, and the final comparison
is also model-generated.

## How the script works

`ask_groq()` builds the chat message list, optionally adding a system message,
and calls Groq with the selected model. All examples use this helper, with
`temperature=0.3` and `max_completion_tokens=2000`. The self-consistency
example calls the helper three times for its initial attempts and once more to
compare them.

The model is selected from `GROQ_MODEL`, falling back to
`openai/gpt-oss-120b` when that variable is not set. Check the Groq console for
models available to your account.

## Requirements

- Python 3
- A Groq API key
- The packages listed in `requirements.txt` (`groq` and `python-dotenv`)

## Setup

From this directory, create and activate a virtual environment if desired,
then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Create a `.env` file in this directory and add your API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Optionally select a model available to your Groq account:

```dotenv
GROQ_MODEL=your_groq_model_id
```

Keep `.env` private; do not commit or share your API key.

## Run

```bash
python main.py
```

Choose options `1` through `5` to run an example, or `6` to exit. Each example
uses the configured Groq API and therefore requires network access and a valid
API key.

## Topics Covered

- **Zero-shot and few-shot prompting:** compare a task-only request with one that includes examples.
- **Role-based prompting:** separate role/style guidance in a system message from concrete task requirements.
- **Reasoning and verification:** request a calculation explanation, then independently check the arithmetic.
- **Repeated sampling:** compare three responses, while recognizing that agreement is not proof of correctness.
- **API-backed chat:** a shared helper sends messages to Groq and prints the returned completion.

## Project Structure

```text
prompt_examples/
├── main.py          # Menu, prompt examples, and Groq API requests
├── requirements.txt # Groq client and python-dotenv
├── .env             # Local GROQ_API_KEY and optional GROQ_MODEL settings
└── README.md
```

The `.env` file is local configuration and must remain private. The source reads `GROQ_MODEL`, defaulting to `openai/gpt-oss-120b`; it requires a valid `GROQ_API_KEY`. There is no automated test suite, and each selected example requires network access.
