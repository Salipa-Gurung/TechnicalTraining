import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from pact import Pact
from client import UserServiceClient

PACT_DIR = os.path.join(os.path.dirname(__file__), "pacts")


@pytest.fixture
def pact():
    pact = Pact("OrderService", "UserService")
    pact.with_specification("V3")
    return pact


def test_get_user(pact):
    (
        pact.upon_receiving("a request for user 1")
        .given("user 1 exists")
        .with_request("GET", "/users/1")
        .will_respond_with(200)
        .with_header("Content-Type", "application/json")
        .with_body({"id": "1", "name": "Alice", "status": "active"})
    )

    with pact.serve() as mock_server:
        client = UserServiceClient(base_url=str(mock_server.url))
        user = client.get_user("1")

        assert user["name"] == "Alice"
        assert user["status"] == "active"

    pact.write_file(PACT_DIR, overwrite=True)
