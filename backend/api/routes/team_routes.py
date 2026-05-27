from fastapi import APIRouter

from backend.utils.stats import (
    get_match_count,
    get_team_win_percentage
)

router = APIRouter(
    prefix="/team",
    tags=["Team"]
)


# ---------------------------------------------------
# Match Count
# ---------------------------------------------------

@router.get("/{team_name}/matches")
def team_matches(team_name: str):

    return get_match_count(team_name)


# ---------------------------------------------------
# Win Percentage
# ---------------------------------------------------

@router.get("/{team_name}/win-percentage")
def team_win_percentage(team_name: str):

    return get_team_win_percentage(team_name)