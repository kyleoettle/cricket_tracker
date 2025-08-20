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

app = FastAPI()

# --- In-memory mock data for sessions ---

# --- In-memory mock data for all entities ---
sessions: list[Session] = []
players: list[Player] = []
cyclelogs: list[CycleLog] = []
teams: list[Team] = []
metrics: list[Metric] = []
injuries: list[Injury] = []
modelregistries: list[ModelRegistry] = []


# --- Session Endpoints ---
@app.get("/sessions", response_model=list[Session])
def list_sessions():
    return sessions


@app.post("/sessions", response_model=Session)
def create_session(session: Session):
    # Convert date string to date object if needed
    if isinstance(session.date, str):
        session.date = datetime.strptime(session.date, "%Y-%m-%d").date()
    session.id = str(uuid4())
    sessions.append(session)
    return session


@app.get("/sessions/{session_id}", response_model=Session)
def get_session(session_id: str):
    for s in sessions:
        if s.id == session_id:
            return s
    raise HTTPException(status_code=404, detail="Session not found")


# --- Player Endpoints ---
@app.get("/players", response_model=list[Player])
def list_players():
    return players


@app.post("/players", response_model=Player)
def create_player(player: Player):
    player.id = str(uuid4())
    players.append(player)
    return player


@app.get("/players/{player_id}", response_model=Player)
def get_player(player_id: str):
    for p in players:
        if p.id == player_id:
            return p
    raise HTTPException(status_code=404, detail="Player not found")


# --- CycleLog Endpoints ---
@app.get("/cyclelogs", response_model=list[CycleLog])
def list_cyclelogs():
    return cyclelogs


@app.post("/cyclelogs", response_model=CycleLog)
def create_cyclelog(cyclelog: CycleLog):
    # Convert period_start string to date object if needed
    if isinstance(cyclelog.period_start, str):
        cyclelog.period_start = datetime.strptime(
            cyclelog.period_start, "%Y-%m-%d"
        ).date()
    cyclelog.id = str(uuid4())
    cyclelogs.append(cyclelog)
    return cyclelog


@app.get("/cyclelogs/{cyclelog_id}", response_model=CycleLog)
def get_cyclelog(cyclelog_id: str):
    for c in cyclelogs:
        if c.id == cyclelog_id:
            return c
    raise HTTPException(status_code=404, detail="CycleLog not found")


# --- Team Endpoints ---
@app.get("/teams", response_model=list[Team])
def list_teams():
    return teams


@app.post("/teams", response_model=Team)
def create_team(team: Team):
    team.id = str(uuid4())
    teams.append(team)
    return team


@app.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: str):
    for t in teams:
        if t.id == team_id:
            return t
    raise HTTPException(status_code=404, detail="Team not found")


# --- Metric Endpoints ---
@app.get("/metrics", response_model=list[Metric])
def list_metrics():
    return metrics


@app.post("/metrics", response_model=Metric)
def create_metric(metric: Metric):
    # Convert week string to date object if needed
    if isinstance(metric.week, str):
        metric.week = datetime.strptime(metric.week, "%Y-%m-%d").date()
    metric.id = str(uuid4())
    metrics.append(metric)
    return metric


@app.get("/metrics/{metric_id}", response_model=Metric)
def get_metric(metric_id: str):
    for m in metrics:
        if m.id == metric_id:
            return m
    raise HTTPException(status_code=404, detail="Metric not found")


# --- Injury Endpoints ---
@app.get("/injuries", response_model=list[Injury])
def list_injuries():
    return injuries


@app.post("/injuries", response_model=Injury)
def create_injury(injury: Injury):
    # Convert date string to date object if needed
    if isinstance(injury.date, str):
        injury.date = datetime.strptime(injury.date, "%Y-%m-%d").date()
    injury.id = str(uuid4())
    injuries.append(injury)
    return injury


@app.get("/injuries/{injury_id}", response_model=Injury)
def get_injury(injury_id: str):
    for i in injuries:
        if i.id == injury_id:
            return i
    raise HTTPException(status_code=404, detail="Injury not found")


# --- ModelRegistry Endpoints ---
@app.get("/modelregistries", response_model=list[ModelRegistry])
def list_modelregistries():
    return modelregistries


@app.post("/modelregistries", response_model=ModelRegistry)
def create_modelregistry(modelregistry: ModelRegistry):
    # Convert trained_at string to date object if needed
    if isinstance(modelregistry.trained_at, str):
        modelregistry.trained_at = datetime.strptime(
            modelregistry.trained_at, "%Y-%m-%d"
        ).date()
    modelregistry.id = str(uuid4())
    modelregistries.append(modelregistry)
    return modelregistry


@app.get("/modelregistries/{modelregistry_id}", response_model=ModelRegistry)
def get_modelregistry(modelregistry_id: str):
    for mr in modelregistries:
        if mr.id == modelregistry_id:
            return mr
    raise HTTPException(status_code=404, detail="ModelRegistry not found")


app = FastAPI()

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
