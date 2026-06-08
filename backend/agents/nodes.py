from .state import AgentState

from backend.tools.player_tools import (
    player_runs_tool,
    player_strike_rate_tool
)

from backend.utils.entity_extractor import (
    extract_player_name
)

from backend.rag.retriever import (
    retrieve_context
)

import ollama


# ----------------------------------
# Entity Extraction Node
# ----------------------------------

def extract_entities_node(state: AgentState):

    state.setdefault("reasoning", [])

    player_name = extract_player_name(
        state["question"]
    )

    state["player_name"] = player_name

    state["reasoning"].append(
        f"Extracted player: {player_name}"
    )

    return state


# ----------------------------------
# Router Node
# ----------------------------------

def router_node(state: AgentState):

    question = state["question"].lower()

    if (
        "analyze" in question
        or "analysis" in question
        or "compare" in question
    ):

        route = "hybrid"

    elif (
        "strike rate" in question
        or "runs" in question
    ):

        route = "stats"

    else:

        route = "rag"

    state["route"] = route

    state["reasoning"].append(
        f"Selected route: {route}"
    )

    print(f"Route Selected: {route}")

    return state


# ----------------------------------
# Stats Node
# ----------------------------------

def stats_node(state: AgentState):

    question = state["question"].lower()

    player_name = state.get("player_name")

    if not player_name:

        state["tool_output"] = {
            "error": "Player not found"
        }

        return state

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

    state["reasoning"].append(
        "Executed stats tool"
    )

    return state


# ----------------------------------
# RAG Node
# ----------------------------------

def rag_node(state: AgentState):

    question = state["question"]

    chunks = retrieve_context(question)

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    state["retrieved_context"] = context

    state["tool_output"] = {
        "source": "rag",
        "chunks": chunks
    }

    state["reasoning"].append(
        f"Retrieved {len(chunks)} chunks"
    )

    return state


# ----------------------------------
# Hybrid Node
# ----------------------------------

def hybrid_node(state: AgentState):

    question = state["question"]

    player_name = state.get("player_name")

    stats = {}

    if player_name:

        stats = {
            "runs": player_runs_tool(
                player_name
            ),
            "strike_rate": player_strike_rate_tool(
                player_name
            )
        }

    chunks = retrieve_context(question)

    context = "\n".join(
        chunk["text"]
        for chunk in chunks
    )

    state["retrieved_context"] = context

    state["tool_output"] = {
        "stats": stats,
        "context": context
    }

    state["reasoning"].append(
        "Executed hybrid workflow"
    )

    return state


# ----------------------------------
# Answer Generation Node
# ----------------------------------

def answer_node(state: AgentState):

    question = state["question"]

    tool_output = state.get(
        "tool_output",
        {}
    )

    reasoning = "\n".join(
        state.get("reasoning", [])
    )

    prompt = f"""
You are an expert cricket analyst.

Question:
{question}

Available Data:
{tool_output}

Reasoning Steps:
{reasoning}

Instructions:
- Use ONLY the provided data.
- Do not hallucinate.
- If information is insufficient, clearly say so.
- Answer naturally and concisely.
"""

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    state["final_answer"] = (
        response["message"]["content"]
    )

    state["reasoning"].append(
        "Generated final answer using Mistral"
    )

    return state