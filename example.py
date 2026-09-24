from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    greeting: str

def create_greeting(state: State):
    return {
        "greeting": "Hello " + state["name"] + "!"
    }

builder = StateGraph(State)
builder.add_node("greeting_node", create_greeting)

builder.add_edge(START, "greeting_node")
builder.add_edge("greeting_node", END)

graph = builder.compile()

result = graph.invoke({
    "name": "Gayatri",
    "greeting": ""
})
print(result)