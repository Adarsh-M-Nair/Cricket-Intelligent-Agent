import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
from sqlalchemy import func

from backend.database.db import SessionLocal
from backend.database.models import Match, Delivery


# ---------------------------------------------------
# Database Session
# ---------------------------------------------------

db = SessionLocal()


# ---------------------------------------------------
# Generate Batting Chunks
# ---------------------------------------------------

def generate_batting_chunks():

    chunks = []

    batters = (
        db.query(
            Delivery.batter,
            func.sum(Delivery.runs).label("total_runs")
        )
        .group_by(Delivery.batter)
        .order_by(func.sum(Delivery.runs).desc())
        .all()
    )

    for index, batter in enumerate(batters):

        player_name = batter[0]

        total_runs = batter[1]

        chunk = {
            "id": f"batting_{index + 1}",

            "text": (
                f"{player_name} scored "
                f"{total_runs} runs in the IPL dataset."
            ),

            "metadata": {
                "player": player_name,
                "type": "batting_stats"
            }
        }

        chunks.append(chunk)

    return chunks


# ---------------------------------------------------
# Generate Match Chunks
# ---------------------------------------------------

def generate_match_chunks():

    chunks = []

    matches = db.query(Match).all()

    for index, match in enumerate(matches):

        text = (
            f"{match.team1} played against "
            f"{match.team2} at {match.venue}. "
            f"{match.winner} won the match."
        )

        chunk = {
            "id": f"match_{index + 1}",

            "text": text,

            "metadata": {
                "match_id": match.match_id,
                "winner": match.winner,
                "type": "match_summary"
            }
        }

        chunks.append(chunk)

    return chunks


# ---------------------------------------------------
# Generate Strike Rate Chunks
# ---------------------------------------------------

def generate_strike_rate_chunks():

    chunks = []

    players = (
        db.query(
            Delivery.batter
        )
        .distinct()
        .all()
    )

    for index, player in enumerate(players):

        player_name = player[0]

        runs = (
            db.query(func.sum(Delivery.runs))
            .filter(Delivery.batter == player_name)
            .scalar()
        )

        balls = (
            db.query(func.count(Delivery.id))
            .filter(Delivery.batter == player_name)
            .scalar()
        )

        runs = runs if runs else 0
        balls = balls if balls else 0

        strike_rate = 0

        if balls > 0:
            strike_rate = round((runs / balls) * 100, 2)

        text = (
            f"{player_name} has a strike rate "
            f"of {strike_rate} in the IPL dataset."
        )

        chunk = {
            "id": f"strike_rate_{index + 1}",

            "text": text,

            "metadata": {
                "player": player_name,
                "strike_rate": strike_rate,
                "type": "strike_rate"
            }
        }

        chunks.append(chunk)

    return chunks


# ---------------------------------------------------
# Save Chunks
# ---------------------------------------------------

def save_chunks(chunks, output_path):

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nChunks saved successfully at:\n{output_path}")


# ---------------------------------------------------
# Main
# ---------------------------------------------------

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    OUTPUT_DIR = BASE_DIR / "data" / "processed"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH = OUTPUT_DIR / "chunks.json"

    print("\nGenerating batting chunks...")
    batting_chunks = generate_batting_chunks()

    print("Generating match chunks...")
    match_chunks = generate_match_chunks()

    print("Generating strike rate chunks...")
    strike_rate_chunks = generate_strike_rate_chunks()

    all_chunks = (
        batting_chunks +
        match_chunks +
        strike_rate_chunks
    )

    print(f"\nTotal Chunks Generated: {len(all_chunks)}")

    save_chunks(all_chunks, OUTPUT_PATH)