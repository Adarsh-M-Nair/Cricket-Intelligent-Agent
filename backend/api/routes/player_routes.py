from fastapi import APIRouter

from backend.utils.stats import (
    get_total_runs,
    get_strike_rate
)

router = APIRouter(
    prefix="/player",
    tags=["Player"]
)


# ---------------------------------------------------
# Total Runs
# ---------------------------------------------------

@router.get("/{player_name}/runs")
def player_total_runs(player_name: str):

    return get_total_runs(player_name)


# ---------------------------------------------------
# Strike Rate
# ---------------------------------------------------

@router.get("/{player_name}/strike-rate")
def player_strike_rate(player_name: str):

    return get_strike_rate(player_name)