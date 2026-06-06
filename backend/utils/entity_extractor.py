import re


def extract_player_name(question: str):

    patterns = [
        r"What is (.*?)'s",
        r"How many runs has (.*?) scored",
        r"Tell me about (.*)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None