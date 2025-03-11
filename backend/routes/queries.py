from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import database
from models import QueryParams, ComparisonRequest

router = APIRouter()

@router.post("/drivers")
async def query_drivers(query_params: QueryParams):
    """Query drivers based on attribute, comparison, and value"""
    try:
        valid_attributes = [
            'age', 'total_pole_positions', 'total_race_wins', 
            'total_points_scored', 'total_world_titles', 'total_fastest_laps'
        ]
        
        if query_params.attribute not in valid_attributes:
            raise HTTPException(status_code=400, detail=f"Invalid attribute. Valid attributes are: {valid_attributes}")
        
        if query_params.comparison not in ['lt', 'gt', 'eq']:
            raise HTTPException(status_code=400, detail="Invalid comparison. Use 'lt', 'gt', or 'eq'")
        
        return await database.query_drivers(
            query_params.attribute, 
            query_params.comparison, 
            query_params.value
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/teams")
async def query_teams(query_params: QueryParams):
    """Query teams based on attribute, comparison, and value"""
    try:
        valid_attributes = [
            'year_founded', 'total_pole_positions', 'total_race_wins', 
            'total_constructor_titles', 'finishing_position_previous_season'
        ]
        
        if query_params.attribute not in valid_attributes:
            raise HTTPException(status_code=400, detail=f"Invalid attribute. Valid attributes are: {valid_attributes}")
        
        if query_params.comparison not in ['lt', 'gt', 'eq']:
            raise HTTPException(status_code=400, detail="Invalid comparison. Use 'lt', 'gt', or 'eq'")
        
        return await database.query_teams(
            query_params.attribute, 
            query_params.comparison, 
            query_params.value
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compare-drivers")
async def compare_drivers(comparison: ComparisonRequest):
    """Compare two drivers"""
    try:
        driver1, driver2 = await database.compare_drivers(comparison.id1, comparison.id2)
        return {"driver1": driver1, "driver2": driver2}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/compare-teams")
async def compare_teams(comparison: ComparisonRequest):
    """Compare two teams"""
    try:
        team1, team2 = await database.compare_teams(comparison.id1, comparison.id2)
        return {"team1": team1, "team2": team2}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))