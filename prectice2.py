from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define State
class State(TypedDict):
    task: str
    count: int
    complete: bool


# 2. Process node
def process(state: State):
    count = state["count"] + 1

    print(f"Processing task... Attempt {count}")

    # Example: task becomes complete after 3 attempts
    if count >= 3:
        complete = True
    else:
        complete = False

    return {
        "count": count,
        "complete": complete
    }


# 3. Check whether task is complete
def check_completion(state: State):
    if state["complete"]:
        return "complete"
    else:
        return "continue"


# 4. Create graph
builder = StateGraph(State)

builder.add_node("process", process)

# START → Process
builder.add_edge(START, "process")

# Process → condition
builder.add_conditional_edges(
    "process",
    check_completion,
    {
        "continue": "process",   # Loop again
        "complete": END          # Finish
    }
)


# 5. Compile
graph = builder.compile()


# 6. Run
result = graph.invoke({
    "task": "Complete my task",
    "count": 0,
    "complete": False
})

print(result)