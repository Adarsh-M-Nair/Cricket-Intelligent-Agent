from langgraph.graph import StateGraph

from .state import AgentState

from .nodes import (
    router_node,
    stats_node,
    rag_node
)


builder = StateGraph(AgentState)


# ----------------------------------
# Nodes
# ----------------------------------

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "stats",
    stats_node
)

builder.add_node(
    "rag",
    rag_node
)


# ----------------------------------
# Entry Point
# ----------------------------------

builder.set_entry_point("router")


# ----------------------------------
# Route Decision Function
# ----------------------------------

def route_decision(state: AgentState):

    return state["route"]


# ----------------------------------
# Conditional Routing
# ----------------------------------

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "stats": "stats",
        "rag": "rag"
    }
)


# ----------------------------------
# Finish Points
# ----------------------------------

builder.set_finish_point("stats")
builder.set_finish_point("rag")


graph = builder.compile()