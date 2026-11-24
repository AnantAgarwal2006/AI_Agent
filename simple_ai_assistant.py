import json
from types import SimpleNamespace
from Utilities.utilities import log
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS, run_tool

load_dotenv()  # by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

# safety limit: the max number of model rounds for one user question
MAX_STEPS = 5

messages.append({
    "role": "system",
    "content": (
        "answer general questions(programming,science,advice) from your own knowledge."
        "use a tool ONLY when the user asks for the current time, weather, city etc."
        "keep answers under 100 words only."
    )
})


def stream_chat(history):
    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        stream=True,
    )

    full_response = ""
    calls = {}
    label_printed = False
# streaming started
    try:
        for chunk in stream:
                if not chunk.choices:
                    continue
        
                delta = chunk.choices[0].delta
        
                # do we have content from the llm
                # content streaming
                if delta.content:
                    if not label_printed:
                        print("Assistant", end="", flush=True)
                        label_printed = True
        
                    print(delta.content, end="", flush=True)
                    full_response += delta.content
        
                # tool calls
                for tc in (delta.tool_calls or []):
                    obj = calls.setdefault(
                        tc.index,
                        SimpleNamespace(
                            id=None,
                            function=SimpleNamespace(
                                name="",
                                arguments=""
                            ),
                        ),
                    )
        
                    if tc.id:
                        obj.id = tc.id
        
                    if tc.function and tc.function.name:
                        obj.function.name = tc.function.name
        
                    if tc.function and tc.function.arguments:
                        obj.function.arguments += tc.function.arguments
    except KeyboardInterrupt:
        print("\nStopped by you")
        calls={}
    if label_printed:
        print()  # move to the next line after the assistant response

    calls_list = []

    for key in sorted(calls):
        calls_list.append(calls[key])
        # run_tool(calls[key])

    return full_response, calls_list


def build_tool_call_payload(tool_calls):
    # it converts our collected tool calls into the dict format that the API expects inside an assistant message
    payload = []

    for tool_call in tool_calls:
        tool_call_dict = {
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments,
            },
        }

        payload.append(tool_call_dict)

    return payload


while True:
    user_input = input("\nUser:")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # chained tool calling
    for step in range(MAX_STEPS):
        full_response, tool_calls = stream_chat(messages)

        if not tool_calls:
            break

        log(f"Step {step + 1}: model requested {len(tool_calls)}")

        messages.append({
            "role": "assistant",
            "content": full_response,
            "tool_calls": build_tool_call_payload(tool_calls)
        })

        for tool_call in tool_calls:
            func_name = tool_call.function.name
            func_args = {}

            result = run_tool(tool_call)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    else:
        # in python else after a for loop only if the loop finishes normally,
        # means it was not ended by a break
        # we ran out of steps and the model cannot give the final answer
        fallback = "sorry, I could not finish this within the step limit"

        messages.append({
            "role": "assistant",
            "content": fallback
        })

        print("Assistant " + fallback)
        continue