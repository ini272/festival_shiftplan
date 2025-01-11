from fastapi.testclient import TestClient
from app.main import app
from app.core.enums import ShiftPlanStatus

client = TestClient(app)

def test_create_shift():
    # Create plan first
    plan_response = client.post(
        "/plans/",
        json={
            "name": "Test Festival",
            "status": ShiftPlanStatus.DRAFT
        }
    )
    plan_id = plan_response.json()["id"]
    
    # Create shift
    shift_response = client.post(
        "/shifts/",
        json={
            "start_time": "2024-02-20T14:00:00",
            "end_time": "2024-02-20T18:00:00",
            "capacity": 2,
            "shift_plan_id": plan_id
        }
    )
    assert shift_response.status_code == 200
    assert shift_response.json()["capacity"] == 2

def test_invalid_shift_plan():
    response = client.post(
        "/shifts/",
        json={
            "start_time": "2024-02-20T14:00:00",
            "end_time": "2024-02-20T18:00:00",
            "capacity": 2,
            "shift_plan_id": 99999
        }
    )
    assert response.status_code == 404
