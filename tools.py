from datetime import datetime 
import requests
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TOOLS=[
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"Returns the current date and time as a formatted string.",
            "parameters":{
                "type":"object",
                "properties":{},
                "required": []
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"this tool returns the current or live wheather  of the given city ",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"city to get the wheather from",
                    }
                }
            }
        }
    }
]

# http://wttr.in   -> free whether service(web API)
def get_city_weather(city):
    url=f"https://wttr.in/{city}?format=3"
    response=requests.get(url,timeout=10)
    return response.text
# how to call in python 
# requests  -> third pparty http library -> not built in python , we have to install it , this helps to send http requests and talk to websites or web apis.
#llm access tool method by name by this functionmap
FUNCTION_NAME_TO_FUNTION_MAP={
    "get_current_time":get_current_time,
    "get_city_weather":get_city_weather,
}
