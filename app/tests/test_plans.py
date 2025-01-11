from fastapi.testclient import TestClient
from app.main import app
from app.core.enums import ShiftPlanStatus

client = TestClient(app)

def test_create_plan():
    response = client.post(
        "/plans/",
        json={
            "name": "Summer Festival",
            "status": ShiftPlanStatus.DRAFT
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Summer Festival"
    assert response.json()["status"] == ShiftPlanStatus.DRAFT

def test_update_plan_status():
    # Create plan
    create_response = client.post(
        "/plans/",
        json={
            "name": "Status Test",
            "status": ShiftPlanStatus.DRAFT
        }
    )
    plan_id = create_response.json()["id"]
    
    # Update to published
    update_response = client.put(
        f"/plans/{plan_id}",
        json={
            "name": "Status Test",
            "status": ShiftPlanStatus.PUBLISHED.value
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == ShiftPlanStatus.PUBLISHED

def test_create_plan_with_group_size():
    response = client.post(
        "/plans/",
        json={
            "name": "Festival with Groups",
            "status": ShiftPlanStatus.DRAFT,
            "max_group_size": 4
        }
    )
    assert response.status_code == 200
    assert response.json()["max_group_size"] == 4

def test_create_plan_default_group_size():
    response = client.post(
        "/plans/",
        json={
            "name": "Default Groups Festival",
            "status": ShiftPlanStatus.DRAFT
        }
    )
    assert response.status_code == 200
    assert response.json()["max_group_size"] == 3
