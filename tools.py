# first we import the standard libraries
import json
# then third party imports
from datetime import datetime
import requests
# then import the local modelues 
# this is the standard pattern for imports
from Utilities.utilities import log
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current date and time as a formatted string.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "this tool returns the current or live wheather of the given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "city to get the wheather from",
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_city",
            "description": "this is the default user city name if explicitly not mentioned by user about it, if explicitly user tells the other city then consider that not this else consider this.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# http://wttr.in -> free whether service(web API)
def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # this will raise HTTPError if something goes wrong
    return response.text


def get_user_city():
    return "agra"


def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}

    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
        log(f" ~{func_name}({func_args})")
        fn = FUNCTION_NAME_TO_FUNTION_MAP[func_name]
        result = fn(**func_args)
    except Exception as e:
        result = f"Error while running {func_name}:{e}"

    log(f"   ~{result}")
    return str(result)

# how to call in python
# requests -> third party http library -> not built in python, we have to install it,
# this helps to send http requests and talk to websites or web apis.

# llm access tool method by name by this function map
FUNCTION_NAME_TO_FUNTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_user_city": get_user_city,
}