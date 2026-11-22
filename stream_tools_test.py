# standard library imports
import os
from types import SimpleNamespace
# SimpleNamespace is a small utility class from Python's built-in types module that lets you create an object whose attributes you can add and access using dot notation.
# Third-party imports
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS,run_tool

load_dotenv() # by default looks for .env file
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

stream = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[{"role": "user", "content": "tell me teh weather of delhi and pune. No need to mention the number of words used."}],
    tools=TOOLS,
    stream=True
)

calls={} #index-> tool call being built

for chunk in stream:
    if not chunk.choices: # some servers send chunks no choices
        continue
    delta=chunk.choices[0].delta
    for tc in (delta.tool_calls or []):
        obj=calls.setdefault(
            tc.index,
            SimpleNamespace(id=None,function=SimpleNamespace(name="",arguments="")),
        )
        if tc.id:
            obj.id=tc.id
        if tc.function and tc.function.name:
            obj.function.name=tc.function.name
        if tc.funtion and tc.function.arguments:
            obj.functions.arguments=tc.functions.arguments

calls_list=[]
for key in sorted(calls):
    calls.list.append(calls[key])
    # run_tool(calls[key])