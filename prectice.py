from typing import TypedDict
from langgraph.graph import START, StateGraph, END

class State(TypedDict):
    a: int
    b: int
    sum: int
    result: int

def add(state: State):
    return {"sum": state["a"] + state["b"]}

def multiply(state: State):
    return {"result": state["sum"] * 10}

builder = StateGraph(State)
builder.add_node("add", add)
builder.add_edge(START, "add")
builder.add_node("multiply", multiply)
builder.add_edge("add", "multiply")
builder.add_edge("multiply", END)

graph = builder.compile()
input_data = {"a":10,  "b": 20,
"sum": 0, "result": 0}
output = graph.invoke(input_data)
print(output)