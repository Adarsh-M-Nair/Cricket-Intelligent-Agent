from fastapi import APIRouter

from backend.utils.stats import get_top_batters

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)


# ---------------------------------------------------
# Top Batters
# ---------------------------------------------------

@router.get("/top-batters")
def top_batters(limit: int = 10):

    return get_top_batters(limit)