import sys
from pathlib import Path
from sqlalchemy import func

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.database.db import SessionLocal
from backend.database.models import Match, Delivery


# ---------------------------------------------------
# Database Session
# ---------------------------------------------------

db = SessionLocal()


# ---------------------------------------------------
# Total Runs by Player
# ---------------------------------------------------

def get_total_runs(player_name):

    total_runs = (
        db.query(func.sum(Delivery.runs))
        .filter(Delivery.batter == player_name)
        .scalar()
    )

    return {
        "player": player_name,
        "total_runs": total_runs if total_runs else 0
    }


# ---------------------------------------------------
# Total Balls Faced
# ---------------------------------------------------

def get_total_balls(player_name):

    total_balls = (
        db.query(func.count(Delivery.id))
        .filter(Delivery.batter == player_name)
        .scalar()
    )

    return {
        "player": player_name,
        "balls_faced": total_balls if total_balls else 0
    }


# ---------------------------------------------------
# Strike Rate
# ---------------------------------------------------

def get_strike_rate(player_name):

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
        strike_rate = (runs / balls) * 100

    return {
        "player": player_name,
        "runs": runs,
        "balls": balls,
        "strike_rate": round(strike_rate, 2)
    }


# ---------------------------------------------------
# Top Batters
# ---------------------------------------------------

def get_top_batters(limit=10):

    batters = (
        db.query(
            Delivery.batter,
            func.sum(Delivery.runs).label("total_runs")
        )
        .group_by(Delivery.batter)
        .order_by(func.sum(Delivery.runs).desc())
        .limit(limit)
        .all()
    )

    result = []

    for batter in batters:

        result.append({
            "player": batter[0],
            "runs": batter[1]
        })

    return result


# ---------------------------------------------------
# Match Count by Team
# ---------------------------------------------------

def get_match_count(team_name):

    matches = (
        db.query(Match)
        .filter(
            (Match.team1 == team_name) |
            (Match.team2 == team_name)
        )
        .count()
    )

    return {
        "team": team_name,
        "matches_played": matches
    }


# ---------------------------------------------------
# Team Win Percentage
# ---------------------------------------------------

def get_team_win_percentage(team_name):

    total_matches = (
        db.query(Match)
        .filter(
            (Match.team1 == team_name) |
            (Match.team2 == team_name)
        )
        .count()
    )

    total_wins = (
        db.query(Match)
        .filter(Match.winner == team_name)
        .count()
    )

    percentage = 0

    if total_matches > 0:
        percentage = (total_wins / total_matches) * 100

    return {
        "team": team_name,
        "matches": total_matches,
        "wins": total_wins,
        "win_percentage": round(percentage, 2)
    }


# ---------------------------------------------------
# Match Summary
# ---------------------------------------------------

def get_match_summary(match_id):

    match = (
        db.query(Match)
        .filter(Match.match_id == str(match_id))
        .first()
    )

    if not match:

        return {
            "error": "Match not found"
        }

    deliveries = (
        db.query(Delivery)
        .filter(Delivery.match_id == str(match_id))
        .all()
    )

    total_runs = sum(delivery.runs for delivery in deliveries)

    total_balls = len(deliveries)

    return {
        "match_id": match.match_id,
        "teams": f"{match.team1} vs {match.team2}",
        "winner": match.winner,
        "venue": match.venue,
        "total_runs": total_runs,
        "total_balls": total_balls
    }


# ---------------------------------------------------
# Main Testing
# ---------------------------------------------------

if __name__ == "__main__":

    print("\n========== TOTAL RUNS ==========")
    print(get_total_runs("Virat Kohli"))

    print("\n========== STRIKE RATE ==========")
    print(get_strike_rate("MS Dhoni"))

    print("\n========== TOP BATTERS ==========")
    print(get_top_batters())

    print("\n========== MATCH COUNT ==========")
    print(get_match_count("Mumbai Indians"))

    print("\n========== TEAM WIN % ==========")
    print(get_team_win_percentage("Chennai Super Kings"))

    print("\n========== MATCH SUMMARY ==========")
    print(get_match_summary("1"))