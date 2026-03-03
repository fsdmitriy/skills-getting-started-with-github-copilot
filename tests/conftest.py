from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture

def client():
    """Provides a TestClient and resets the in-memory state after each test.

    The FastAPI application stored its global ``activities`` dictionary in
    ``src.app.activities``.  We take a deep copy before yielding the client and
    restore it afterwards so individual tests can't leak state into one
    another.  ``TestClient`` itself is created inside the fixture so each test
    gets a fresh instance.
    """

    original = deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    try:
        yield client
    finally:
        app_module.activities.clear()
        app_module.activities.update(original)
