import json
from urllib.request import Request, urlopen


class Client:
    def __init__(self, base_url: str, api_token: str, user_agent: str):
        self._base_url = base_url
        self._api_token = api_token
        self._user_agent = user_agent

    def call_api(self, endpoint: str, payload: dict):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = f"{self._base_url}{endpoint}"

        json_data = json.dumps(payload).encode()
        req = Request(url, data=json_data, method="POST")
        req.add_header("Authorization", f"Bearer {self._api_token}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", self._user_agent)

        with urlopen(req) as response:
            response_data = response.read().decode()

        print(f"Response: {response_data}")

    def call_service(self, domain: str, service: str, entity_id: str):
        self.call_api(
            endpoint=f"/api/services/{domain}/{service}",
            payload={
                "entity_id": entity_id,
            },
        )
