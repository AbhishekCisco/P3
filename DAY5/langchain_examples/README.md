# LangChain Tool-Calling Agent with Groq

## Purpose

`langchain_examples.py` is a small interactive command-line chatbot. It sends each question to a Groq-hosted language model through LangChain. When useful, the model can request one of three Python tools: get the current time, calculate an expression, or compute averages from a CSV file. Conversation history is kept while the program is running.

This example demonstrates how a language model, a prompt, tools, memory, and an agent executor can work together. It is an educational example, not a production-ready service.

## Learning Objectives

- Connect a chat model to Python functions exposed as tools.
- Understand how an agent executor coordinates model requests and tool results.
- Keep conversation messages in process-local memory during one chat run.
- Inspect the security and reliability boundaries created by calculator and file-reading tools.

## Requirements and Setup

Use Python 3.10 or later. From this directory, install the packages used by the script:

```bash
python -m pip install python-dotenv pandas langchain-groq langchain-core langchain-classic
```

Create a `.env` file in this directory and put your Groq API key in it:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Keep `.env` private and do not commit it to source control. The script raises an error at startup if `GROQ_API_KEY` is unavailable. The configured model must also be available to the Groq account.

Start the chat from this directory so the sample CSV path resolves as expected:

```bash
python langchain_examples.py
```

Type a question at the `You:` prompt. Enter `exit` to end the process. Example prompts:

- `What time is it?`
- `What is 100 * (2 + 3)?`
- `What are the average values in sales.csv?`

The CSV tool accepts a file path supplied by the agent. Relative paths are resolved from the program's current working directory. The included `sales.csv` has average `price` 150 and average `quantity` 3.

## What the Script Does

1. Loads variables from `.env`, overriding same-named environment variables because `override=True` is set.
2. Checks that `GROQ_API_KEY` exists and stops with `ValueError` if it does not.
3. Defines three Python functions and exposes them as LangChain tools with `@tool`.
4. Creates conversation memory, the Groq chat model, and a prompt with slots for chat history and agent reasoning/tool-call messages.
5. Builds a tool-calling agent and wraps it in an `AgentExecutor`.
6. Repeatedly reads a user message, invokes the executor, and prints its output. The executor can ask the model to call a tool, return the tool result to the model, and continue until it has a final response.

## Code Reference

### Imports and Their Roles

- `from dotenv import load_dotenv`: imports `load_dotenv`, which reads key/value settings from `.env` into the process environment.
- `import os`: provides `os.getenv`, used to read `GROQ_API_KEY` without hard-coding the secret.
- `import datetime`: provides `datetime.datetime.now()` for the time tool.
- `import pandas as pd`: imports pandas under the conventional alias `pd`; the CSV tool uses it to read and summarize tabular data.
- `from langchain_groq import ChatGroq`: imports the LangChain chat-model wrapper for the Groq API.
- `from langchain_core.tools import tool`: imports the `tool` decorator that turns Python functions into tools the model can call, using their names, parameter signatures, and docstrings as tool information.
- `from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder`: imports prompt-building classes. `ChatPromptTemplate` combines message templates; `MessagesPlaceholder` inserts a list of messages such as history or the agent scratchpad.
- `from langchain_classic.memory import ConversationBufferMemory`: imports memory that stores the conversation messages for the running chain.
- `AgentExecutor` and `create_tool_calling_agent` from `langchain_classic.agents`: the factory builds an agent that can call tools; the executor runs the agent/tool cycle.

### Startup Configuration

- `load_dotenv(override=True)`: loads `.env` before the API key is checked. With `override=True`, a value in `.env` takes precedence over an already-set process environment value with the same name.
- `os.getenv("GROQ_API_KEY")`: returns the key if set, otherwise `None`.
- `raise ValueError(...)`: fails fast with a readable message if the key is missing, rather than waiting for a later API request to fail.

### Tools

Each function below is decorated with `@tool`. The decorator exposes the function to the agent; the function's docstring helps describe when and how to use it.

#### `get_current_time(dummy: str = "") -> str`

Calls `datetime.datetime.now()` and returns the resulting local date and time as a string. `dummy` is an unused string argument with a default value, included as the tool's input schema. The agent can choose this tool for questions about the current time.

#### `calculator(expression: str) -> str`

Evaluates a mathematical expression and returns text such as `Result = 12`. `allowed_names` makes `abs`, `round`, `min`, and `max` available to the expression. `eval` is called with an empty `__builtins__` mapping to restrict built-in names. The `try`/`except` catches evaluation errors and returns them as `Error: ...` text instead of raising them out of the tool.

**Security note:** restricting built-ins is not a robust sandbox for Python `eval`. Do not use this implementation with untrusted expressions or expose it as-is in a public service. A production calculator should parse and allow only explicitly supported syntax, for example with a dedicated expression parser or a carefully validated abstract syntax tree.

#### `analyze_csv(file_path: str) -> str`

Uses `pd.read_csv(file_path)` to load a CSV into a pandas `DataFrame`. `df.mean(numeric_only=True)` calculates the mean of each numeric column, and `to_string()` formats those means as text. Non-numeric columns are excluded. Read or processing failures are caught and returned as `Error reading CSV: ...` text.

The tool reads paths available to the Python process. In a real application, validate and constrain paths so an agent cannot read files outside the intended data directory.

### Agent Configuration

- `ConversationBufferMemory(memory_key="chat_history", return_messages=True)`: stores prior conversation turns under the `chat_history` key and returns them as message objects. This memory is in process only; it is not saved after the program exits.
- `ChatGroq(model="openai/gpt-oss-120b", temperature=0)`: configures the chat model. `temperature=0` requests more consistent, less varied outputs; it does not guarantee identical responses. The model still needs API access through the configured Groq key.
- `tools = [...]`: collects the three decorated tools and makes the same tool set available to both the agent factory and executor.
- `ChatPromptTemplate.from_messages([...])`: creates a sequence of messages for the model. The system message describes the assistant, `{input}` is replaced by the current user message, and the two placeholders are populated at runtime.
- `MessagesPlaceholder(variable_name="chat_history")`: inserts prior conversation messages from memory.
- `MessagesPlaceholder(variable_name="agent_scratchpad")`: gives the agent a place for intermediate messages, including its tool-call requests and tool results, while it works on the current turn.
- `create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)`: connects the model, tool definitions, and prompt into a tool-calling agent.
- `AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)`: runs the agent, dispatches requested tool calls, coordinates memory, and returns a final result. `verbose=True` prints intermediate execution details to the console.

### Chat Loop and Methods

- `print(...)`: displays the welcome message and tool list.
- `while True`: keeps the command-line chat running until the user exits.
- `input("You: ")`: waits for the next user message.
- `user_input.lower() == "exit"`: compares the command without regard to letter case. On a match, the script prints a goodbye and `break` ends the loop.
- `agent_executor.invoke({"input": user_input})`: submits one turn to the agent executor. The dictionary supplies the prompt's `input` variable. The returned dictionary contains the final text under `response["output"]`.
- `try`/`except Exception as e`: catches errors from a turn, such as API or executor errors, and prints the error while allowing the chat loop to continue.

## Important Concepts and Learning Outcomes

### What Is an Agent?

An agent is a program that uses a language model to decide how to respond or what action to take. Here, `create_tool_calling_agent` gives the model the available tool descriptions. The model can answer directly or request a tool call; `AgentExecutor` performs that call and lets the model use its result to prepare a response. The model chooses when and which tool to request, but the Python functions perform the actual operations.

### What Is a Tool?

A tool is a named, described function that an agent can invoke for a task. Tools give a language model access to capabilities outside text generation, such as reading a dataset or getting the machine's current time. In this example `@tool` packages each function so LangChain can describe its arguments and call it. Tool inputs and permissions should be validated because tools act with the permissions of the Python process.

### Other Ideas Demonstrated

- **Tool calling:** the model requests a named operation with structured arguments; the application runs it and returns its result to the model.
- **Prompt templates:** reusable message structures separate system instructions, conversation history, current input, and intermediate agent messages.
- **Conversation memory:** previous turns can inform later responses during one run. `ConversationBufferMemory` keeps the full buffer in memory, so a long conversation can grow over time.
- **Model configuration:** a model name and temperature control which chat model is called and how varied its outputs may be.
- **Data analysis with pandas:** a few DataFrame operations load a CSV and compute numeric-column averages.
- **Error handling:** exceptions are converted to readable tool or chat errors, though returning errors as text means the agent may need to interpret them.
- **Secrets management:** API credentials belong in environment configuration, not source code.
- **Trust boundaries:** an agent's tool calls should be treated as untrusted input. Validate expressions, constrain file access, and limit tool permissions before using this pattern beyond a local learning exercise.

## Limitations

- The conversation is lost when the process exits.
- The calculator's `eval` approach is not safe for untrusted input.
- The CSV tool accepts a path and has no allowlist or directory restriction.
- The script has no authentication, rate limiting, persistent storage, or automated tests.
- `temperature=0` and a tool description do not guarantee that the model will always choose the correct tool or interpret its output correctly.

## Project Structure

```text
langchain_examples/
├── langchain_examples.py # Tool definitions, agent setup, and interactive chat loop
├── sales.csv             # Small sample for numeric-column averaging
├── .env                  # Local Groq key/model settings; keep private
└── README.md
```

The folder currently has no `requirements.txt`; the setup command above installs the packages directly. A local `venv/` directory may also be present, but it is an environment containing installed third-party packages, not part of the learning source.

## Configuration and Data Notes

- The source requires `GROQ_API_KEY` and loads `.env` with `override=True`. The file also has a `GROQ_MODEL` setting, but the code currently hard-codes `openai/gpt-oss-120b` in `ChatGroq`, so changing `GROQ_MODEL` does not change the selected model.
- Run the script from this folder when asking the agent to analyze `sales.csv`; relative paths resolve from the current working directory.
- The sample CSV has numeric `price` and `quantity` columns. The documented averages are 150 and 3, respectively.
- No automated tests are included, and API calls require network access and a model available to the configured Groq account.