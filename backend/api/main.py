from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.player_routes import router as player_router
from api.routes.team_routes import router as team_router
from api.routes.match_routes import router as match_router
from api.routes.stats_routes import router as stats_router
from api.routes.rag_routes import router as rag_router

app = FastAPI(
    title="Cricket Intelligence Agent API",
    description="Cricket Analytics and AI Backend",
    version="1.0.0"
)

# -----------------------------------------
# CORS
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------
# Root Endpoint
# -----------------------------------------

@app.get("/")
def home():
    return {
        "message": "Cricket Intelligence Agent API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# -----------------------------------------
# Register API Routes
# -----------------------------------------

app.include_router(player_router)
app.include_router(team_router)
app.include_router(match_router)
app.include_router(stats_router)
app.include_router(rag_router)