import os
import json
from urllib.request import Request, urlopen

HA_API_TOKEN = os.environ["HA_API_TOKEN"]


def ha_api(endpoint: str, payload: dict):
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    url = f"https://home-assistant.snow.jflei.com{endpoint}"

    json_data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=json_data, method="POST")
    req.add_header("Authorization", f"Bearer {HA_API_TOKEN}")
    req.add_header("Content-Type", "application/json")

    with urlopen(req) as response:
        response_data = response.read().decode("utf-8")

    print(f"Response: {response_data}")


def ha_service(domain: str, service: str, entity_id: str):
    ha_api(
        endpoint=f"/api/services/{domain}/{service}",
        payload={
            "entity_id": entity_id,
        },
    )


ha_service(
    domain="switch",
    service="toggle",
    entity_id="switch.garage_outlet_storage_underside_lights",
)
