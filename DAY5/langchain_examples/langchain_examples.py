from dotenv import load_dotenv
load_dotenv(override=True)


import os
import datetime
import pandas as pd


from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)




# -----------------------------------
# VALIDATE API KEY
# -----------------------------------
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found in .env file")




# -----------------------------------
# TOOL 1 - CURRENT TIME TOOL
# -----------------------------------
@tool
def get_current_time(dummy: str = "") -> str:
    """Returns the current date and time."""
    return str(datetime.datetime.now())




# -----------------------------------
# TOOL 2 - CALCULATOR TOOL
# -----------------------------------
@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression."""


    try:
        # Only use eval with trusted, restricted expressions.
        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max
        }


        result = eval(
            expression,
            {"__builtins__": {}},
            allowed_names
        )


        return f"Result = {result}"


    except Exception as e:
        return f"Error: {str(e)}"




# -----------------------------------
# TOOL 3 - CSV ANALYZER
# -----------------------------------
@tool
def analyze_csv(file_path: str) -> str:
    """Reads a CSV file and returns averages of numeric columns."""


    try:
        df = pd.read_csv(file_path)


        numeric_means = df.mean(numeric_only=True)


        return numeric_means.to_string()


    except Exception as e:
        return f"Error reading CSV: {str(e)}"




# -----------------------------------
# MEMORY
# -----------------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)




# -----------------------------------
# GROQ MODEL
# -----------------------------------
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)




# -----------------------------------
# TOOLS
# -----------------------------------
tools = [
    get_current_time,
    calculator,
    analyze_csv
]




# -----------------------------------
# PROMPT
# -----------------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant with tool calling abilities. "
            "Use the available tools whenever required."
        ),


        MessagesPlaceholder(
            variable_name="chat_history"
        ),


        ("human", "{input}"),


        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        )
    ]
)




# -----------------------------------
# CREATE GROQ TOOL-CALLING AGENT
# -----------------------------------
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)




# -----------------------------------
# AGENT EXECUTOR
# -----------------------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)




# -----------------------------------
# CHAT LOOP
# -----------------------------------
print("\nAdvanced Groq LangChain Agent Started")
print("Available tools:")
print("1. Current Time")
print("2. Calculator")
print("3. CSV Analyzer")
print("Type 'exit' to stop\n")




while True:


    user_input = input("You: ")


    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break


    try:


        response = agent_executor.invoke({
            "input": user_input
        })


        print("\nBot Response:")
        print("--------------------------------")
        print(response["output"])
        print("--------------------------------\n")


    except Exception as e:
        print(f"\nError: {str(e)}\n")
