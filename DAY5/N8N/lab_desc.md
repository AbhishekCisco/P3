step 6.1 . run n8n docker image
step 6.2 open n8n server and create a workflow select ai agent and add option : system message and then paste the below text:
    You are an intelligent AI Calculator Assistant.

You can answer general questions directly.

You have access to a Python Calculator API tool.

Whenever the user requests mathematical calculations:
1. Identify the operation.
2. Identify the first number.
3. Identify the second number.
4. Call the Python Calculator API tool.
5. Use the API response to provide the final answer.

Supported operations:
- add
- subtract
- multiply
- divide

Do not calculate the result yourself.
Always use the Python API for calculations.


Step 6.3. Connect Groq Chat Model
Click the Chat Model connector below the AI Agent.
Select Groq Chat Model.
Create new Groq credentials.
Enter your Groq API key.
Select a tool-calling-capable model, such as openai/gpt-oss-120b, if available in your model list.
Set temperature to 0.
The Groq Chat Model is responsible for understanding user requests and deciding when to invoke the API tool.
Nodes+1
Step 6.4. Add HTTP Request Tool
This is the most important step.
The HTTP Request Tool allows your AI Agent to communicate with your Python FastAPI application.
Click the Tool connector below AI Agent.
Search for HTTP Request.
Select the HTTP Request tool.
Configure the following settings.
HTTP Request Tool configuration
Configure the HTTP Request node connected to the AI Agent's Tool connector.
Tool name
python_calculator
HTTP Method
POST
URL
http://host.docker.internal:8000/calculate
Authentication
None (for this local demo)
Send Body
Enabled
Body Content Type
JSON
Configure the JSON request body
Configure the three parameters as follows:
Parameter 1: operation
Setting
Value
Name
operation
Value
Expression


{{ $fromAI('operation', 'Arithmetic operation: add, subtract, multiply or divide', 'string') }}
Parameter 2: a
Setting
Value
Name
a
Value
Expression


{{ $fromAI('a', 'First number', 'number') }}
Parameter 3: b
Setting
Value
Name
b
Value
Expression


{{ $fromAI('b', 'Second number', 'number') }}
The $fromAI() function allows the model to dynamically populate the tool parameters from the user's request.
n8n Documentation
For example, if the user asks:
Calculate 250 * 45
The agent supplies:
{
  "operation": "multiply",
  "a": 250,
  "b": 45
}
The HTTP Request Tool sends this JSON to your Python API.
Step 6.5. Connect the nodes
Your final n8n workflow should look like this:
Chat Trigger
User message
AI Agent
Decides whether to use Python API
Groq Chat Model
Chat Model connector
HTTP Request Tool
Tool connector
Python FastAPI
POST /calculate
Note: Groq Chat Model and HTTP Request Tool are connected through the AI Agent's respective model and tool connectors, not as ordinary sequential workflow nodes.
7. Test your AI Agent
Save the workflow and click Execute Workflow or open the Chat Trigger's chat interface.
Try the following questions:
Test cases
Test 1: Calculate 250 multiplied by 45
Expected result: 11,250
Test 2: Add 500 and 250
Expected result: 750
Test 3: Subtract 150 from 500
Expected result: 350
Test 4: Divide 1000 by 25
Expected result: 40
Test 5: What happens if I divide 100 by zero?
Expected result: Division by zero error from Python API
