from typing import TypedDict

class AgentState(TypedDict, total=False):

    question: str

    player_name: str

    route: str

    retrieved_context: str

    tool_output: dict

    final_answer: str

    reasoning: list