import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.parser import CricketMatchParser

from backend.database.db import SessionLocal, engine, Base
from backend.database.models import Match, Delivery


# Create database tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")


def load_matches_to_database(dataset_path):

    parser = CricketMatchParser(dataset_path)
    print(f"\nLoading dataset from: {dataset_path}")

    matches = parser.parse_all_matches()

    db = SessionLocal()

    try:

        for match in matches:

            match_info = match["match_info"]

            innings_data = match["innings_data"]

            # -----------------------------
            # Insert Match Information
            # -----------------------------

            db_match = Match(
                match_id=str(match_info["match_id"]),
                date=str(match_info["date"]),
                venue=match_info["venue"],
                team1=match_info["team1"],
                team2=match_info["team2"],
                winner=match_info["winner"]
            )

            db.add(db_match)

            # -----------------------------
            # Insert Ball-by-Ball Data
            # -----------------------------

            for delivery in innings_data:

                db_delivery = Delivery(
                    match_id=str(match_info["match_id"]),
                    innings=delivery["innings"],
                    over=delivery["over"],
                    ball=delivery["ball"],
                    batter=delivery["batter"],
                    bowler=delivery["bowler"],
                    runs=delivery["total_runs"]
                )

                db.add(db_delivery)

        # Commit all records
        db.commit()

        print("\nAll matches loaded successfully into database.")

    except Exception as e:

        db.rollback()

        print(f"\nError loading data: {e}")

    finally:

        db.close()


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    DATASET_PATH = BASE_DIR / "data" / "raw" / "ipl" / "ipl_json"

    print(f"\nDataset Path: {DATASET_PATH}")

    load_matches_to_database(DATASET_PATH)