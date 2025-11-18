from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.models.models import (
    Player,
    Session,
    CycleLog,
    Team,
    Metric,
    Injury,
    ModelRegistry,
)

from uuid import uuid4
from datetime import datetime
from src.services.cosmos import get_db


app = FastAPI()
db = get_db()

# --- In-memory mock data for sessions ---

# --- In-memory mock data for all entities ---
sessions: list[Session] = []
players: list[Player] = []
cyclelogs: list[CycleLog] = []
teams: list[Team] = []
metrics: list[Metric] = []
injuries: list[Injury] = []
modelregistries: list[ModelRegistry] = []


# --- Session Endpoints (Cosmos DB) ---
@app.get("/sessions", response_model=list[Session])
def list_sessions():
    query = "SELECT * FROM c"
    items = db.query_items("sessions", query)
    return items


@app.post("/sessions", response_model=Session)
def create_session(session: Session):
    if isinstance(session.date, str):
        session.date = datetime.strptime(session.date, "%Y-%m-%d").date()
    session.id = str(uuid4())
    item = session.model_dump()
    db.upsert_item("sessions", item)
    return session


@app.get("/sessions/{session_id}", response_model=Session)
def get_session(session_id: str):
    # Partition key is player_id
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [{"name": "@id", "value": session_id}]
    items = db.query_items("sessions", query, params)
    if items:
        return items[0]
    raise HTTPException(status_code=404, detail="Session not found")


# --- Player Endpoints (Cosmos DB) ---
@app.get("/players", response_model=list[Player])
def list_players():
    query = "SELECT * FROM c"
    items = db.query_items("players", query)
    return items


@app.post("/players", response_model=Player)
def create_player(player: Player):
    player.id = str(uuid4())
    item = player.dict()
    db.upsert_item("players", item)
    return player


@app.get("/players/{player_id}", response_model=Player)
def get_player(player_id: str):
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [{"name": "@id", "value": player_id}]
    items = db.query_items("players", query, params)
    if items:
        return items[0]
    raise HTTPException(status_code=404, detail="Player not found")


# --- CycleLog Endpoints (Cosmos DB) ---
@app.get("/cyclelogs", response_model=list[CycleLog])
def list_cyclelogs():
    query = "SELECT * FROM c"
    items = db.query_items("cycleLogs", query)
    return items


@app.post("/cyclelogs", response_model=CycleLog)
def create_cyclelog(cyclelog: CycleLog):
    if isinstance(cyclelog.period_start, str):
        cyclelog.period_start = datetime.strptime(
            cyclelog.period_start, "%Y-%m-%d"
        ).date()
    cyclelog.id = str(uuid4())
    item = cyclelog.model_dump()
    db.upsert_item("cycleLogs", item)
    return cyclelog


@app.get("/cyclelogs/{cyclelog_id}", response_model=CycleLog)
def get_cyclelog(cyclelog_id: str):
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [{"name": "@id", "value": cyclelog_id}]
    items = db.query_items("cycleLogs", query, params)
    if items:
        return items[0]
    raise HTTPException(status_code=404, detail="CycleLog not found")


# --- Team Endpoints (Cosmos DB) ---
@app.get("/teams", response_model=list[Team])
def list_teams():
    query = "SELECT * FROM c"
    items = db.query_items("teams", query)
    return items


@app.post("/teams", response_model=Team)
def create_team(team: Team):
    team.id = str(uuid4())
    item = team.dict()
    db.upsert_item("teams", item)
    return team


@app.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: str):
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [{"name": "@id", "value": team_id}]
    items = db.query_items("teams", query, params)
    if items:
        return items[0]
    raise HTTPException(status_code=404, detail="Team not found")


# --- Metric Endpoints (Cosmos DB) ---
@app.get("/metrics", response_model=list[Metric])
def list_metrics():
    query = "SELECT * FROM c"
    items = db.query_items("metrics", query)
    return items


@app.post("/metrics", response_model=Metric)
def create_metric(metric: Metric):
    if isinstance(metric.week, str):
        metric.week = datetime.strptime(metric.week, "%Y-%m-%d").date()
    metric.id = str(uuid4())
    item = metric.dict()
    db.upsert_item("metrics", item)
    return metric


@app.get("/metrics/{metric_id}", response_model=Metric)
def get_metric(metric_id: str):
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [{"name": "@id", "value": metric_id}]
    items = db.query_items("metrics", query, params)
    if items:
        return items[0]
    raise HTTPException(status_code=404, detail="Metric not found")


# --- Injury Endpoints (Cosmos DB) ---
@app.get("/injuries", response_model=list[Injury])
def list_injuries():
    query = "SELECT * FROM c"
    items = db.query_items("injuries", query)
    return items


@app.post("/injuries", response_model=Injury)
def create_injury(injury: Injury):
    if isinstance(injury.date, str):
        injury.date = datetime.strptime(injury.date, "%Y-%m-%d").date()
    injury.id = str(uuid4())
    item = injury.dict()
    db.upsert_item("injuries", item)
    return injury


@app.get("/injuries/{injury_id}", response_model=Injury)
def get_injury(injury_id: str):
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [{"name": "@id", "value": injury_id}]
    items = db.query_items("injuries", query, params)
    if items:
        return items[0]
    raise HTTPException(status_code=404, detail="Injury not found")


# --- ModelRegistry Endpoints (Cosmos DB) ---
@app.get("/modelregistries", response_model=list[ModelRegistry])
def list_modelregistries():
    query = "SELECT * FROM c"
    items = db.query_items("modelRegistry", query)
    return items


@app.post("/modelregistries", response_model=ModelRegistry)
def create_modelregistry(modelregistry: ModelRegistry):
    if isinstance(modelregistry.trained_at, str):
        modelregistry.trained_at = datetime.strptime(
            modelregistry.trained_at, "%Y-%m-%d"
        ).date()
    modelregistry.id = str(uuid4())
    item = modelregistry.dict()
    db.upsert_item("modelRegistry", item)
    return modelregistry


@app.get("/modelregistries/{modelregistry_id}", response_model=ModelRegistry)
def get_modelregistry(modelregistry_id: str):
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [{"name": "@id", "value": modelregistry_id}]
    items = db.query_items("modelRegistry", query, params)
    if items:
        return items[0]
    raise HTTPException(status_code=404, detail="ModelRegistry not found")


# CORS setup (for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- JWT Auth Middleware (placeholder) ---
# def jwt_auth_middleware(request: Request):
#     # TODO: Implement JWT validation
#     pass

# --- RBAC Decorator (placeholder) ---
# def require_role(role: str):
#     def decorator(func):
#         # TODO: Implement role-based access control
#         return func
#     return decorator


@app.get("/health", response_class=JSONResponse)
def health_check() -> dict:
    """
    Health check endpoint for API status.
    Returns:
        dict: Status message.
    """
    return {"status": "ok"}


# Future: include routers for sessions, cycle logs, metrics, etc.
