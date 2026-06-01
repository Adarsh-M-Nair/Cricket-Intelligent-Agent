from fastapi import APIRouter

from utils.stats import get_match_summary

router = APIRouter(
    prefix="/match",
    tags=["Match"]
)


# ---------------------------------------------------
# Match Summary
# ---------------------------------------------------

@router.get("/{match_id}")
def match_summary(match_id: str):

    return get_match_summary(match_id)