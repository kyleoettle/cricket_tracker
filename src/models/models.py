from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class Player(BaseModel):
    id: Optional[str] = None
    name: str
    role: str
    team_id: Optional[str]
    email: Optional[str]


class Session(BaseModel):
    id: Optional[str] = None
    player_id: str
    date: date
    session_type: str
    duration: int
    rpe: int
    batting_minutes: int
    bowling_overs: int
    fielding_time: int
    comment: Optional[str]


class CycleLog(BaseModel):
    id: Optional[str] = None
    player_id: str
    period_start: date
    symptoms: List[str]
    wellness: int
    sleep: int
    mood: int
    soreness: int
    comment: Optional[str]


class Team(BaseModel):
    id: Optional[str] = None
    name: str
    player_ids: List[str]


class Metric(BaseModel):
    id: Optional[str] = None
    player_id: str
    week: date
    acute: int
    chronic: int
    acwr: float


class Injury(BaseModel):
    id: Optional[str] = None
    player_id: str
    date: date
    type: str
    severity: str
    description: Optional[str]


class ModelRegistry(BaseModel):
    id: Optional[str] = None
    model_name: str
    version: str
    trained_at: date
    accuracy: Optional[float]
    notes: Optional[str]
