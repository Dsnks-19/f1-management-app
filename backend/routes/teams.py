from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from models import TeamCreate, Team, TeamUpdate
import database
from auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Team)
async def create_team(team: TeamCreate, user: Dict = Depends(get_current_user)):
    """Create a new team (requires authentication)"""
    try:
        return await database.create_team(team)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Team])
async def read_teams():
    """Get all teams (no authentication required)"""
    return await database.get_all_teams()

@router.get("/{team_id}", response_model=Team)
async def read_team(team_id: str):
    """Get a specific team by ID (no authentication required)"""
    team = await database.get_team(team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.put("/{team_id}", response_model=Team)
async def update_team(team_id: str, team_update: TeamUpdate, user: Dict = Depends(get_current_user)):
    """Update a team (requires authentication)"""
    try:
        team = await database.update_team(team_id, team_update)
        if team is None:
            raise HTTPException(status_code=404, detail="Team not found")
        return team
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{team_id}")
async def delete_team(team_id: str, user: Dict = Depends(get_current_user)):
    """Delete a team (requires authentication)"""
    try:
        result = await database.delete_team(team_id)
        if not result:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"message": "Team deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))