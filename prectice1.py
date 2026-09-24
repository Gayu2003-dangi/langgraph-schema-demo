from typing import TypedDict
from langgraph.graph import START, StateGraph, END


# State
class State(TypedDict):
    query: str
    category: str
    answer: str
    a: int
    b: int


# Classifier
def classifier(state: State):
    query = state["query"].lower()

    if "code" in query or "python" in query:
        return {"category": "coding"}

    elif "math" in query or "sum" in query or "add" in query:
        return {"category": "math"}

    else:
        return {"category": "general"}


# This function tells LangGraph which route was selected
def route_category(state: State):
    return state["category"]


# Coding Node
def Coding(state: State):
    return {
        "answer": "This is a coding question."
    }


# Math Node
def Math(state: State):
    return {
        "answer": f"The sum of {state['a']} and {state['b']} is {state['a'] + state['b']}"
    }


# General Node
def General(state: State):
    return {
        "answer": "This is a general question."
    }


# Create graph
builder = StateGraph(State)


# Add nodes
builder.add_node("Classifier_node", classifier)
builder.add_node("Coding_node", Coding)
builder.add_node("Math_node", Math)
builder.add_node("General_node", General)


# START → Classifier
builder.add_edge(START, "Classifier_node")


# Classifier → appropriate node
builder.add_conditional_edges(
    "Classifier_node",
    route_category,
    {
        "coding": "Coding_node",
        "math": "Math_node",
        "general": "General_node"
    }
)


# Nodes → END
builder.add_edge("Coding_node", END)
builder.add_edge("Math_node", END)
builder.add_edge("General_node", END)

# Compile
graph = builder.compile()

# Run
result = graph.invoke({
    "query": "Add two numbers",
    "a": 10,
    "b": 20
})

print(result)