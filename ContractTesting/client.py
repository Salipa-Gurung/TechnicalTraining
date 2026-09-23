import requests


class UserServiceClient:
    """Consumer: OrderService's client for talking to UserService."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_user(self, user_id: str) -> dict:
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()
