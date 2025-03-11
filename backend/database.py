from firebase_admin import firestore
from typing import List, Dict, Any, Optional, Tuple
from models import DriverCreate, TeamCreate, DriverUpdate, TeamUpdate
import uuid

db = firestore.client()

# Driver collections
drivers_ref = db.collection('drivers')
teams_ref = db.collection('teams')

# Driver functions
async def create_driver(driver: DriverCreate) -> Dict[str, Any]:
    """Create a new driver in Firestore"""
    # Check if driver with same name exists
    existing_drivers = drivers_ref.where('name', '==', driver.name).limit(1).get()
    if len(existing_drivers) > 0:
        raise ValueError(f"Driver with name '{driver.name}' already exists")
    
    # Check if team exists
    team_docs = teams_ref.where('name', '==', driver.team).limit(1).get()
    if len(team_docs) == 0:
        raise ValueError(f"Team '{driver.team}' does not exist")

    driver_id = str(uuid.uuid4())
    driver_dict = driver.dict()
    drivers_ref.document(driver_id).set(driver_dict)
    
    return {"id": driver_id, **driver_dict}

async def get_all_drivers() -> List[Dict[str, Any]]:
    """Get all drivers from Firestore"""
    drivers = []
    for doc in drivers_ref.stream():
        drivers.append({"id": doc.id, **doc.to_dict()})
    return drivers

async def get_driver(driver_id: str) -> Optional[Dict[str, Any]]:
    """Get a driver by ID from Firestore"""
    doc = drivers_ref.document(driver_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return None

async def update_driver(driver_id: str, driver_update: DriverUpdate) -> Optional[Dict[str, Any]]:
    """Update a driver in Firestore"""
    doc = drivers_ref.document(driver_id).get()
    if not doc.exists:
        return None
    
    update_data = {k: v for k, v in driver_update.dict().items() if v is not None}
    
    # If team is being updated, check if it exists
    if 'team' in update_data:
        team_docs = teams_ref.where('name', '==', update_data['team']).limit(1).get()
        if len(team_docs) == 0:
            raise ValueError(f"Team '{update_data['team']}' does not exist")
    
    drivers_ref.document(driver_id).update(update_data)
    
    updated_doc = drivers_ref.document(driver_id).get()
    return {"id": updated_doc.id, **updated_doc.to_dict()}

async def delete_driver(driver_id: str) -> bool:
    """Delete a driver from Firestore"""
    doc = drivers_ref.document(driver_id).get()
    if not doc.exists:
        return False
    
    drivers_ref.document(driver_id).delete()
    return True

async def query_drivers(attribute: str, comparison: str, value: Any) -> List[Dict[str, Any]]:
    """Query drivers based on attribute, comparison, and value"""
    # Convert value to appropriate type based on attribute
    if attribute in ['age', 'total_pole_positions', 'total_race_wins', 'total_points_scored', 
                    'total_world_titles', 'total_fastest_laps']:
        value = int(value)
    
    result = []
    # Firestore doesn't support dynamic field comparisons directly
    # So we'll get all documents and filter them in Python
    docs = drivers_ref.stream()
    
    for doc in docs:
        doc_data = doc.to_dict()
        # Check if the document matches the query
        if attribute in doc_data:
            if comparison == 'eq' and doc_data[attribute] == value:
                result.append({"id": doc.id, **doc_data})
            elif comparison == 'lt' and doc_data[attribute] < value:
                result.append({"id": doc.id, **doc_data})
            elif comparison == 'gt' and doc_data[attribute] > value:
                result.append({"id": doc.id, **doc_data})
    
    return result

# Team functions
async def create_team(team: TeamCreate) -> Dict[str, Any]:
    """Create a new team in Firestore"""
    # Check if team with same name exists
    existing_teams = teams_ref.where('name', '==', team.name).limit(1).get()
    if len(existing_teams) > 0:
        raise ValueError(f"Team with name '{team.name}' already exists")
    
    team_id = str(uuid.uuid4())
    team_dict = team.dict()
    teams_ref.document(team_id).set(team_dict)
    
    return {"id": team_id, **team_dict}

async def get_all_teams() -> List[Dict[str, Any]]:
    """Get all teams from Firestore"""
    teams = []
    for doc in teams_ref.stream():
        teams.append({"id": doc.id, **doc.to_dict()})
    return teams

async def get_team(team_id: str) -> Optional[Dict[str, Any]]:
    """Get a team by ID from Firestore"""
    doc = teams_ref.document(team_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return None

async def update_team(team_id: str, team_update: TeamUpdate) -> Optional[Dict[str, Any]]:
    """Update a team in Firestore"""
    doc = teams_ref.document(team_id).get()
    if not doc.exists:
        return None
    
    update_data = {k: v for k, v in team_update.dict().items() if v is not None}
    teams_ref.document(team_id).update(update_data)
    
    updated_doc = teams_ref.document(team_id).get()
    return {"id": updated_doc.id, **updated_doc.to_dict()}

async def delete_team(team_id: str) -> bool:
    """Delete a team from Firestore"""
    doc = teams_ref.document(team_id).get()
    if not doc.exists:
        return False
    
    # Check if any drivers are associated with this team
    team_name = doc.to_dict().get('name')
    drivers_with_team = drivers_ref.where('team', '==', team_name).limit(1).get()
    if len(drivers_with_team) > 0:
        raise ValueError(f"Cannot delete team '{team_name}' as it has associated drivers")
    
    teams_ref.document(team_id).delete()
    return True

async def query_teams(attribute: str, comparison: str, value: Any) -> List[Dict[str, Any]]:
    """Query teams based on attribute, comparison, and value"""
    # Convert value to appropriate type based on attribute
    if attribute in ['year_founded', 'total_pole_positions', 'total_race_wins', 
                    'total_constructor_titles', 'finishing_position_previous_season']:
        value = int(value)
    
    result = []
    # Firestore doesn't support dynamic field comparisons directly
    # So we'll get all documents and filter them in Python
    docs = teams_ref.stream()
    
    for doc in docs:
        doc_data = doc.to_dict()
        # Check if the document matches the query
        if attribute in doc_data:
            if comparison == 'eq' and doc_data[attribute] == value:
                result.append({"id": doc.id, **doc_data})
            elif comparison == 'lt' and doc_data[attribute] < value:
                result.append({"id": doc.id, **doc_data})
            elif comparison == 'gt' and doc_data[attribute] > value:
                result.append({"id": doc.id, **doc_data})
    
    return result

async def compare_drivers(driver_id1: str, driver_id2: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Get two drivers for comparison"""
    driver1 = await get_driver(driver_id1)
    driver2 = await get_driver(driver_id2)
    
    if not driver1 or not driver2:
        raise ValueError("One or both drivers not found")
    
    return driver1, driver2

async def compare_teams(team_id1: str, team_id2: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Get two teams for comparison"""
    team1 = await get_team(team_id1)
    team2 = await get_team(team_id2)
    
    if not team1 or not team2:
        raise ValueError("One or both teams not found")
    
    return team1, team2