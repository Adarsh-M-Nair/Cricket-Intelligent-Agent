from fastapi import FastAPI

from backend.api.routes.player_routes import router as player_router
from backend.api.routes.team_routes import router as team_router
from backend.api.routes.match_routes import router as match_router
from backend.api.routes.stats_routes import router as stats_router


# ---------------------------------------------------
# Create FastAPI App
# ---------------------------------------------------

app = FastAPI(
    title="Cricket Intelligence Agent API",
    description="Cricket Analytics and AI Backend",
    version="1.0.0"
)


# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Cricket Intelligence Agent API is running"
    }


# ---------------------------------------------------
# Register API Routes
# ---------------------------------------------------

app.include_router(player_router)

app.include_router(team_router)

app.include_router(match_router)

app.include_router(stats_router)