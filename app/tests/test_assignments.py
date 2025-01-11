from fastapi.testclient import TestClient
from app.main import app
from app.core.enums import Role, ShiftPlanStatus, PreferenceType

client = TestClient(app)

def test_create_assignment():
    # Setup: Create plan, shift, and crew member
    plan = client.post("/plans/", json={"name": "Test Plan", "status": ShiftPlanStatus.DRAFT})
    shift = client.post(
        "/shifts/",
        json={
            "start_time": "2024-02-20T14:00:00",
            "end_time": "2024-02-20T18:00:00",
            "capacity": 1,
            "shift_plan_id": plan.json()["id"]
        }
    )
    crew = client.post(
        "/crew/",
        json={
            "name": "Test Crew",
            "role": Role.CREW
        }
    )
    
    response = client.post(
        "/assignments/",
        json={
            "shift_id": shift.json()["id"],
            "crew_member_id": crew.json()["id"]
        }
    )
    assert response.status_code == 200

def test_capacity_warning():
    # Setup: Create plan and shift with capacity 1
    plan = client.post("/plans/", json={"name": "Capacity Test", "status": ShiftPlanStatus.DRAFT})
    shift = client.post(
        "/shifts/",
        json={
            "start_time": "2024-02-20T14:00:00",
            "end_time": "2024-02-20T18:00:00",
            "capacity": 1,
            "shift_plan_id": plan.json()["id"]
        }
    )
    
    # Create two crew members
    crew1 = client.post(
        "/crew/",
        json={
            "name": "Crew 1",
            "role": Role.CREW
        }
    )
    crew2 = client.post(
        "/crew/",
        json={
            "name": "Crew 2",
            "role": Role.CREW
        }
    )
    
    # First assignment
    response1 = client.post(
        "/assignments/",
        json={
            "shift_id": shift.json()["id"],
            "crew_member_id": crew1.json()["id"]
        }
    )
    assert response1.status_code == 200
    
    # Second assignment (over capacity)
    response2 = client.post(
        "/assignments/",
        json={
            "shift_id": shift.json()["id"],
            "crew_member_id": crew2.json()["id"]
        }
    )
    assert response2.status_code == 200  # Allows but should log warning
