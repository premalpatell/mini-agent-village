import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"

def calculator(expression):
    if not set(expression) <= set("0123456789+-*/(). "):
        return "Error: only numbers and + - * / ( ) are allowed. For powers use **, e.g. 2 ** 10"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

tools = [{
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Work out an arithmetic expression in Python syntax, e.g. '23 * (4 + 5)'. Use ** for powers, not ^.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The maths to work out"},
            },
            "required": ["expression"],
        },
    },
}]

messages = [
    {"role": "system", "content": "You are a helpful assistant. Always use the calculator for arithmetic."},
    {"role": "user", "content": "What is 1234 * 5678, plus 99?"},
]
for step in range(5):
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print("Answer:", message.content)
        break

    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        result = calculator(args["expression"])
        print(f"Tool: calculator({args['expression']}) = {result}")
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
