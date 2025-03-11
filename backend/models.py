from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any

class DriverBase(BaseModel):
    name: str
    age: int
    total_pole_positions: int
    total_race_wins: int
    total_points_scored: int
    total_world_titles: int
    total_fastest_laps: int
    team: str

class DriverCreate(DriverBase):
    @validator('name')
    def validate_unique_name(cls, name):
        # Note: Actual validation is done in the route handler
        return name

class DriverUpdate(BaseModel):
    age: Optional[int] = None
    total_pole_positions: Optional[int] = None
    total_race_wins: Optional[int] = None
    total_points_scored: Optional[int] = None
    total_world_titles: Optional[int] = None
    total_fastest_laps: Optional[int] = None
    team: Optional[str] = None

class Driver(DriverBase):
    id: str

class TeamBase(BaseModel):
    name: str
    year_founded: int
    total_pole_positions: int
    total_race_wins: int
    total_constructor_titles: int
    finishing_position_previous_season: int

class TeamCreate(TeamBase):
    @validator('name')
    def validate_unique_name(cls, name):
        # Note: Actual validation is done in the route handler
        return name

class TeamUpdate(BaseModel):
    year_founded: Optional[int] = None
    total_pole_positions: Optional[int] = None
    total_race_wins: Optional[int] = None
    total_constructor_titles: Optional[int] = None
    finishing_position_previous_season: Optional[int] = None

class Team(TeamBase):
    id: str

class QueryParams(BaseModel):
    attribute: str
    comparison: str  # "lt", "gt", "eq"
    value: Any

class ComparisonRequest(BaseModel):
    id1: str
    id2: str