import os
from pact import Verifier

PACT_FILE = os.path.join(
    os.path.dirname(__file__), "pacts", "OrderService-UserService.json"
)


def test_verify_provider():
    verifier = (
        Verifier("UserService")
        .add_transport(url="http://localhost:5001")
        .add_source(PACT_FILE)
    )

    verifier.verify()  # raises if verification fails
