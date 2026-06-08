from langgraph.graph import StateGraph

from .state import AgentState

from .nodes import (
    extract_entities_node,
    router_node,
    stats_node,
    rag_node,
    answer_node
)

builder = StateGraph(AgentState)

builder.add_node("extract", extract_entities_node)
builder.add_node("router", router_node)
builder.add_node("stats", stats_node)
builder.add_node("rag", rag_node)
builder.add_node(
    "answer",
    answer_node
)

builder.set_entry_point("extract")

builder.add_edge(
    "extract",
    "router"
)
builder.add_edge(
    "stats",
    "answer"
)

builder.add_edge(
    "rag",
    "answer"
)

def route_decision(state: AgentState):
    return state["route"]

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "stats": "stats",
        "rag": "rag"
    }
)

builder.set_finish_point(
    "answer"
)

graph = builder.compile()