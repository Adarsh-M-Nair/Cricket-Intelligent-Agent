from .state import AgentState

from backend.tools.player_tools import (
    player_runs_tool,
    player_strike_rate_tool
)
from backend.utils.entity_extractor import extract_player_name
from backend.rag.retriever import retrieve_context


def extract_entities_node(state):

    player_name = extract_player_name(
        state["question"]
    )

    state["player_name"] = player_name

    return state

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

    player_name = state["player_name"]

    if "strike rate" in question:

        result = player_strike_rate_tool(
            player_name
        )

    elif "runs" in question:

        result = player_runs_tool(
            player_name
        )

    else:

        result = {
            "message": "Unsupported stats query"
        }

    state["tool_output"] = result

    return state


# ----------------------------------
# RAG Node 
# ----------------------------------

def rag_node(state: AgentState):

    question = state["question"]

    retrieved_chunks = retrieve_context(question)

    state["tool_output"] = {
        "source": "rag",
        "chunks": retrieved_chunks
    }

    return state