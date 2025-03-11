from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any
from models import DriverCreate, Driver, DriverUpdate
import database
from auth import get_current_user, is_authenticated

router = APIRouter()

@router.post("/", response_model=Driver)
async def create_driver(driver: DriverCreate, user: Dict = Depends(get_current_user)):
    """Create a new driver (requires authentication)"""
    try:
        return await database.create_driver(driver)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Driver])
async def read_drivers():
    """Get all drivers (no authentication required)"""
    return await database.get_all_drivers()

@router.get("/{driver_id}", response_model=Driver)
async def read_driver(driver_id: str):
    """Get a specific driver by ID (no authentication required)"""
    driver = await database.get_driver(driver_id)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.put("/{driver_id}", response_model=Driver)
async def update_driver(driver_id: str, driver_update: DriverUpdate, user: Dict = Depends(get_current_user)):
    """Update a driver (requires authentication)"""
    try:
        driver = await database.update_driver(driver_id, driver_update)
        if driver is None:
            raise HTTPException(status_code=404, detail="Driver not found")
        return driver
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{driver_id}")
async def delete_driver(driver_id: str, user: Dict = Depends(get_current_user)):
    """Delete a driver (requires authentication)"""
    result = await database.delete_driver(driver_id)
    if not result:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver deleted successfully"}