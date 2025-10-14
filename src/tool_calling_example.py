import json
from openai import OpenAI

# Connect to LM Studio’s local endpoint
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")


# Define a simple tool
def calculate_sum(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


# Tool Schema definition
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Add two numbers together and return the sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    }
]


# Instruct model to use the tool
messages = [
    {
        "role": "system",
        "content": "You are a stubborn person who refuses to use tools to help you.",
    },
    {"role": "user", "content": "Add 15.5 and 20.3"},
]

response = client.chat.completions.create(
    model="meta-llama-3-8b-instruct",
    messages=messages,
    tools=tools,
    tool_choice="auto",  # Let the model decide when to call a tool
)


message = response.choices[0].message
if message.tool_calls:
    tool_call = message.tool_calls[0]
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"LLM called: {fn_name}({args})")

    # Execute the function
    if fn_name == "calculate_sum":
        result = calculate_sum(**args)
    else:
        result = "Unknown tool"

    # Send the result back to the model
    messages.append(message)  # include the model's tool call
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result),
        }
    )

    followup = client.chat.completions.create(
        model="meta-llama-3-8b-instruct",
        messages=messages,
    )

    print("Agent’s final reply:", followup.choices[0].message.content)

else:
    print("No tool call detected.")
