from typing import TypedDict
from langgraph.graph import START, StateGraph, END


class State(TypedDict):
    question: str
    search_query: str
    search_results: list
    enough_information: bool
    summary: str


# 1. Generate Query
def generate_query(state: State):
    question = state["question"]

    return {
        "search_query": "Information about " + question
    }


# 2. Search
def search(state: State):
    query = state["search_query"]

    # Dummy search results for practice
    results = [
        "Result 1: Basic information about " + query,
        "Result 2: Detailed information about " + query
    ]

    return {
        "search_results": results
    }


# 3. Evaluate
def evaluate(state: State):
    results = state["search_results"]

    if len(results) >= 2:
        return {
            "enough_information": True
        }

    return {
        "enough_information": False
    }


# 4. Decide whether to search again or summarize
def decide(state: State):

    if state["enough_information"]:
        return "summarize"

    return "search_again"


# 5. Summarize
def summarize(state: State):
    results = state["search_results"]

    summary = " | ".join(results)

    return {
        "summary": summary
    }

# Create graph
builder = StateGraph(State)
builder.add_node("generate_query", generate_query)
builder.add_node("search", search)
builder.add_node("evaluate", evaluate)
builder.add_node("summarize", summarize)

# START → Generate Query
builder.add_edge(START, "generate_query")

# Generate Query → Search
builder.add_edge("generate_query", "search")

# Search → Evaluate
builder.add_edge("search", "evaluate")

# Evaluate → conditional decision
builder.add_conditional_edges(
    "evaluate",
    decide,
    {
        "search_again": "search",
        "summarize": "summarize"
    }
)

# Summarize → END
builder.add_edge("summarize", END)

# Compile
graph = builder.compile()

# Run
result = graph.invoke({
    "question": "LangGraph",
    "search_query": "",
    "search_results": [],
    "enough_information": False,
    "summary": ""
})
print(result)