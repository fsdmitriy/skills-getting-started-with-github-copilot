"""Basic tests exercising the FastAPI backend.

These tests follow the Arrange-Act-Assert (AAA) pattern and use the
``client`` fixture defined in ``tests/conftest.py``.  The fixture ensures that
changes to the global ``activities`` dictionary are discarded between tests.
"""


def test_root_redirects_to_static_index(client):
    # Arrange: nothing special – client fixture already set up
    # Act
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code == 307
    assert resp.headers["location"] == "/static/index.html"


def test_get_activities_contains_known_activity(client):
    # Arrange: pick a name that exists in the default data set
    expected = "Chess Club"
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    assert expected in resp.json()


def test_signup_for_activity_happy_path(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Signed up" in data["message"]
    # make sure the participant is actually recorded
    assert email in client.get("/activities").json()[activity]["participants"]


def test_unregister_happy_path(client):
    # Arrange: sign someone up first so there is something to remove
    activity = "Chess Club"
    email = "another@example.com"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Unregistered" in data["message"]
    assert email not in client.get("/activities").json()[activity]["participants"]
