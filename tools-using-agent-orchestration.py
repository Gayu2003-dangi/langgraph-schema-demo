import os 
import requests
#annotated use kiya h taki new message ko add kar le
from typing import Annotated 
from typing_extensions import TypedDict
from dotenv import load_dotenv 
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

@tool
def get_weather(city: str) -> str:
    """Get the current real weather for a city."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}, timeout=10,
        ).json()
        if "results" not in geo:
            return f"City '{city}' not found"
        place = geo["results"][0]
        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": place["latitude"], "longitude": place["longitude"],
                    "current": "temperature_2m,wind_speed_10m"}, timeout=10,
        ).json()["current"]
        return f"{city}: {w['temperature_2m']}°C, wind {w['wind_speed_10m']} km/h"
    except Exception as e:  # network down etc. -> tell the agent instead of crashing
        return f"Weather API error: {e}"

tools = [get_weather]

#---------------model initialization----------------
model = ChatOpenAI(
    model="gpt-5.6-luna",
    base_url="https://api.experientiallabs.ai/v1",
    api_key=os.environ.get("EXPERIENTAL_LABS_API_KEY"),

).bind_tools(tools) 




def call_model(state):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

#-------------------------------graph construction------------------------------
builder=StateGraph(State)
builder.add_node("call_model", call_model)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "call_model")
builder.add_conditional_edges(
    "call_model",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge("tools","call_model")

graph=builder.compile()

if __name__ == "__main__":
    questione = "What is the weather in New York?"

    for step in graph.stream(
        {"messages": [("user", questione)]},
        stream_mode="updates"
    ):
        for node, update in step.items():
            print(f"\n----- {node} -----")
            update["messages"][-1].pretty_print()
import os 
import requests
#annotated use kiya h taki new message ko add kar le
from typing import Annotated 
from typing_extensions import TypedDict
from dotenv import load_dotenv 
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

@tool
def get_weather(city: str) -> str:
    """Get the current real weather for a city."""
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}, timeout=10,
        ).json()
        if "results" not in geo:
            return f"City '{city}' not found"
        place = geo["results"][0]
        w = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": place["latitude"], "longitude": place["longitude"],
                    "current": "temperature_2m,wind_speed_10m"}, timeout=10,
        ).json()["current"]
        return f"{city}: {w['temperature_2m']}°C, wind {w['wind_speed_10m']} km/h"
    except Exception as e:  # network down etc. -> tell the agent instead of crashing
        return f"Weather API error: {e}"

tools = [get_weather]

#---------------model initialization----------------
model = ChatOpenAI(
    model="gpt-5.6-luna",
    base_url="https://api.experientiallabs.ai/v1",
    api_key=os.environ.get("EXPERIENTAL_LABS_API_KEY"),

).bind_tools(tools) 




def call_model(state):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

#-------------------------------graph construction------------------------------
builder=StateGraph(State)
builder.add_node("call_model", call_model)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "call_model")
builder.add_conditional_edges(
    "call_model",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge("tools","call_model")

graph=builder.compile()

if __name__ == "__main__":
    questione = "What is the weather in New York?"

    for step in graph.stream(
        {"messages": [("user", questione)]},
        stream_mode="updates"
    ):
        for node, update in step.items():
            print(f"\n----- {node} -----")
            update["messages"][-1].pretty_print()