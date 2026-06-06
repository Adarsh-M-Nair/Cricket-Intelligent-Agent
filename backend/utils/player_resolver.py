from functools import lru_cache

from rapidfuzz import process, fuzz

from backend.database.db import SessionLocal
from backend.database.models import Delivery


# ----------------------------------
# Known Player Aliases
# ----------------------------------

PLAYER_ALIASES = {
    "virat kohli": "V Kohli",
    "rohit sharma": "RG Sharma",
    "ishant sharma": "I Sharma",
    "ms dhoni": "MS Dhoni",
    "hardik pandya": "HH Pandya",
    "jasprit bumrah": "JJ Bumrah",
    "suryakumar yadav": "SA Yadav",
    "kl rahul": "KL Rahul",
    "ravindra jadeja": "RA Jadeja",
    "ruturaj gaikwad": "RD Gaikwad"
}


# ----------------------------------
# Load Players Once
# ----------------------------------

@lru_cache(maxsize=1)
def get_all_players():

    db = SessionLocal()

    players = (
        db.query(Delivery.batter)
        .distinct()
        .order_by(Delivery.batter)
        .all()
    )

    db.close()

    return [player[0] for player in players]


# ----------------------------------
# Resolve Player Name
# ----------------------------------

def resolve_player_name(user_input: str):

    if not user_input:
        return None

    normalized_name = user_input.strip().lower()

    # Step 1: Exact alias lookup
    if normalized_name in PLAYER_ALIASES:
        return PLAYER_ALIASES[normalized_name]

    # Step 2: Fuzzy search fallback
    players = get_all_players()

    match = process.extractOne(
        user_input,
        players,
        scorer=fuzz.token_sort_ratio
    )

    # match format:
    # ('V Kohli', score, index)

    if match and match[1] >= 80:
        return match[0]

    # Step 3: No reliable match
    return user_input