# Health Check and Calculator API for n8n

## Overview

This folder contains a small FastAPI service that provides a status response and performs basic arithmetic for an n8n AI Agent workflow. The service is the Python tool endpoint in the DAY5 N8N exercise: the agent sends structured operation and number values to the API, then uses the returned result in its reply.

## Learning Objectives

- Define API request data with Pydantic and restrict allowed operations with `Literal`.
- Implement simple HTTP endpoints with FastAPI.
- Return a useful client error for an invalid calculation such as division by zero.
- Connect an n8n HTTP Request Tool to a Python API running on the host machine.

## Topics Covered

- **Health/status response:** `GET /` returns a short message confirming that the API is running. There is no separate `/health` endpoint.
- **Request validation:** `CalculationRequest` requires an operation (`add`, `subtract`, `multiply`, or `divide`) and two floating-point values.
- **Arithmetic endpoint:** `POST /calculate` returns the operation, both input values, and the result.
- **Error responses:** unsupported operations or invalid field types are rejected by FastAPI/Pydantic with HTTP `422`; division by zero returns HTTP `400`.
- **Service integration:** the n8n HTTP Request Tool calls this API at `http://host.docker.internal:8000/calculate` when running with the parent Compose configuration.

## Project Structure

```text
health_check_api/
├── api.py      # FastAPI app, request schema, status route, and calculator
└── README.md
```

The associated n8n setup is in the parent folder: `../compose.yaml` runs n8n, and `../lab_desc.md` contains the workflow instructions and example prompts. The API itself does not depend on or import n8n.

## Setup and Run

Use Python 3. Install FastAPI and Uvicorn in an environment of your choice; this folder does not currently include a `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install fastapi uvicorn
```

Run the API from this folder on port 8000:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://127.0.0.1:8000/docs` to inspect and try the endpoints. `GET http://127.0.0.1:8000/` should return `{"message":"Python Calculator API is running"}`.

For the n8n integration, start the parent Compose project from `DAY5/N8N` with `docker compose up -d`. The Compose file adds the `host.docker.internal` host-gateway mapping so the container can reach the API on the host. Configure an n8n HTTP Request Tool with method `POST`, URL `http://host.docker.internal:8000/calculate`, JSON body fields `operation`, `a`, and `b`. See `../lab_desc.md` for the AI Agent, Groq model, and `$fromAI()` parameter setup.

## Example Request and Response

Request:

```json
{
  "operation": "multiply",
  "a": 250,
  "b": 45
}
```

Successful response:

```json
{
  "operation": "multiply",
  "number1": 250.0,
  "number2": 45.0,
  "result": 11250.0
}
```

For division by zero, the API responds with HTTP `400` and the detail `Division by zero is not allowed`. The n8n agent can present that tool error to the user; it should not calculate the result itself if following the lab's system instructions.

## Current Limitations

- There is no automated test suite, dependency lock, or `requirements.txt`.
- The API has no authentication, authorization, rate limiting, or input-size controls. It is an educational local service, not a public calculator endpoint.
- Binding to `0.0.0.0` allows the Docker container to reach the service through the host gateway, but can also expose it on other network interfaces. Use only on a trusted local network and do not forward port 8000 publicly.
- The `--reload` option is for development. Remove it for a production deployment and add appropriate access controls.

## What to Study Next

Try the four supported operations through `/docs`, inspect the `422` and `400` responses, then call the same endpoint from the n8n HTTP Request Tool. Add API tests for normal calculations, invalid operations, missing fields, and division by zero before extending the service.