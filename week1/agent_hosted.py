import ast
import json
import operator
import os
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}

# Walks the parsed maths instead of eval(), so only numbers and + - * / ** run.
def evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left, right = evaluate(node.left), evaluate(node.right)
        if isinstance(node.op, ast.Pow) and (abs(right) > 100 or abs(left) > 10**100):
            raise ValueError("number too big. Keep powers to ** 100 or less")
        return OPS[type(node.op)](left, right)
    raise ValueError("only numbers and + - * / ** ( ) are allowed")

def calculator(expression):
    if not set(expression) <= set("0123456789+-*/(). "):
        return "Error: only numbers and + - * / ( ) are allowed. For powers use **, e.g. 2 ** 10"
    try:
        return str(evaluate(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"

def get_today():
    return date.today().strftime("%A %d %B %Y")



functions = {"calculator": calculator, "get_today": get_today}


tools = [
    {
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_today",
            "description": "Get today's real date. Use this for any question about today, the current date, or the current year.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

messages = [
    {"role": "system", "content": "You are a helpful assistant. Always use the calculator for arithmetic."},
    {"role": "user", "content": "What year is it? How many years until 2030?"},
]
for step in range(5):
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print("Answer:", message.content)
        break
    for call in message.tool_calls:
        name = call.function.name
        try:
            args = json.loads(call.function.arguments)
            result = functions[name](**args)
        except Exception as e:
            result = f"Error calling {name}: {e}"
        print(f"Tool: {name}({call.function.arguments}) = {result}")
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})