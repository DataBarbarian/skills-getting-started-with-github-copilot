import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity = "Chess Club"
    email = "duplicate.student@mergington.edu"

    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200

    duplicate = client.post(f"/activities/{activity}/signup?email={email}")
    assert duplicate.status_code == 400
    assert "already signed up" in duplicate.json()["detail"].lower()


def test_unregister_participant_removes_their_email():
    activity = "Science Club"
    email = "remove.me@mergington.edu"

    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200

    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"

    activities = client.get("/activities")
    assert email not in activities.json()[activity]["participants"]
