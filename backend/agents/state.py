from typing import TypedDict

class AgentState(TypedDict):

    question: str

    route: str

    tool_output: dict

    final_answer: str