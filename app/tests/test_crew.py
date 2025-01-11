from fastapi.testclient import TestClient
from app.main import app
from app.core.enums import Role, ShiftPlanStatus, PreferenceType

client = TestClient(app)

def test_create_crew_member():
    response = client.post(
        "/crew/",
        json={
            "name": "John Doe",
            "role": Role.CREW
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_create_crew_group():
    # Create a shift plan first for max_group_size
    plan_response = client.post(
        "/plans/",
        json={
            "name": "Test Festival",
            "status": ShiftPlanStatus.DRAFT
        }
    )
    plan_id = plan_response.json()["id"]

    response = client.post(
        "/crew/groups/",
        json={
            "name": "Test Group",
            "member_names": ["Alice", "Bob", "Charlie"],
            "role": Role.CREW
        },
        params={"shift_plan_id": plan_id}
    )
    assert response.status_code == 200
    assert len(response.json()["members"]) == 3

def test_group_size_limit():
    plan_response = client.post(
        "/plans/",
        json={
            "name": "Size Limit Test",
            "status": ShiftPlanStatus.DRAFT,
            "max_group_size": 2
        }
    )
    plan_id = plan_response.json()["id"]

    response = client.post(
        "/crew/groups/",
        json={
            "name": "Too Large Group",
            "member_names": ["Alice", "Bob", "Charlie"],
            "role": Role.CREW
        },
        params={"shift_plan_id": plan_id}
    )
    assert response.status_code == 400

def test_update_crew_member():
    # Create crew member first
    create_response = client.post(
        "/crew/",
        json={
            "name": "Jane Doe",
            "role": Role.CREW
        }
    )
    crew_id = create_response.json()["id"]
    
    # Update to coordinator
    update_response = client.put(
        f"/crew/{crew_id}",
        json={
            "name": "Jane Smith",
            "role": Role.COORDINATOR
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Jane Smith"
    assert update_response.json()["role"] == Role.COORDINATOR

def test_get_nonexistent_crew():
    response = client.get("/crew/99999")
    assert response.status_code == 404

def test_create_crew_preference():
    # Create crew member and shift first
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
    crew = client.post("/crew/", json={"name": "Test Crew", "role": Role.CREW})
    
    response = client.post(
        f"/crew/{crew.json()['id']}/preferences/",
        json={
            "preference_type": PreferenceType.AVOID,
            "crew_member_id": crew.json()["id"],
            "shift_id": shift.json()["id"]
        }
    )
    assert response.status_code == 200
    assert response.json()["preference_type"] == PreferenceType.AVOID

def test_create_group_preference():
    # Create plan, shift and group first
    plan = client.post("/plans/", json={"name": "Test Plan", "status": ShiftPlanStatus.DRAFT})
    shift = client.post(
        "/shifts/",
        json={
            "start_time": "2024-02-20T14:00:00",
            "end_time": "2024-02-20T18:00:00",
            "capacity": 2,
            "shift_plan_id": plan.json()["id"]
        }
    )
    group = client.post(
        "/crew/groups/",
        json={
            "name": "Test Group",
            "member_names": ["Alice", "Bob"],
            "role": Role.CREW
        },
        params={"shift_plan_id": plan.json()["id"]}
    )
    
    response = client.post(
        f"/crew/groups/{group.json()['id']}/preferences/",
        json={
            "preference_type": PreferenceType.AVOID,
            "group_id": group.json()["id"],
            "shift_id": shift.json()["id"]
        }
    )
    assert response.status_code == 200
    assert response.json()["preference_type"] == PreferenceType.AVOID