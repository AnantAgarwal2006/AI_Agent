import json
from Utilities.utilities import log
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS,run_tool
load_dotenv() # by default looks for .env file
client=OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
messages=[]
# safety limit: the max number of model rounds for ONe user question
MAX_STEPS=5
messages.append({
    "role":"system",
    "content":("answer general questiosn(programming,science,advice)from your own knowledge."
    "use a tool ONLY when the user asks for the current time,wheather,city etc."
    "keep answers under 100 words only.")
})
while True:
    user_input=input("\nUser:")
    if user_input.lower() in ["exit","quit","bye","goodbye"]:
        break
    messages.append(
            {
                "role":"user",
                "content":user_input
            }
    )
    # chained tool calling 
    for step in range(MAX_STEPS):
        response=client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
        )
        msg=response.choices[0].message.content
        if not msg.tool_calls:
            break
        log(f"Step{step+1}:model requested {len(msg.tool_calls)}")
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name=tool_call.function.name
            func_args={}
            result=run_tool(tool_call)
            messages.append({
                "role":"tool",
                "tool_call_id" : tool_call.id,
                "content":str(result),

            })
    else:
        # in python else after a for loop only if the loop finishes normally, means it wa not ended by a break
        # we ran out of steps and the model cannot able to give the final answer
        fallback="sorry,I could not finish this within the step limit"
        messages.append({
            "role":"assistant",
            "content":fallback
        })
        continue
    messages.append({
        "role":"assistant",
        "content":msg.content
    })
    print("Assistant:"+ (msg.content or ""))