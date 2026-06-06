# utils/player_resolver.py

from rapidfuzz import process

from backend.database.db import SessionLocal
from backend.database.models import Delivery


def get_all_players():

    db = SessionLocal()

    players = (
        db.query(Delivery.batter)
        .distinct()
        .all()
    )

    db.close()

    return [player[0] for player in players]


def resolve_player_name(user_input: str):

    players = get_all_players()

    match = process.extractOne(
        user_input,
        players
    )

    if match:
        return match[0]

    return user_input