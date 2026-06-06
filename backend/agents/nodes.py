from .state import AgentState

from tools.player_tools import (
    player_runs_tool,
    player_strike_rate_tool
)


# ----------------------------------
# Router Node
# ----------------------------------

def router_node(state: AgentState):

    question = state["question"].lower()

    if "strike rate" in question:
        route = "stats"

    elif "runs" in question:
        route = "stats"

    else:
        route = "rag"

    state["route"] = route

    print(f"Route Selected: {route}")

    return state


# ----------------------------------
# Stats Node
# ----------------------------------

def stats_node(state: AgentState):

    question = state["question"].lower()

    if "strike rate" in question:

        result = player_strike_rate_tool(
            "Virat Kohli"
        )

    else:

        result = player_runs_tool(
            "Virat Kohli"
        )

    state["tool_output"] = result

    return state


# ----------------------------------
# RAG Node (Temporary)
# ----------------------------------

def rag_node(state: AgentState):

    state["tool_output"] = {
        "source": "rag",
        "message": "RAG Search Executed"
    }

    return state