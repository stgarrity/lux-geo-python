"""API for Lux Thermostat."""

import json
from helpers import http_request


class LuxAPI:
    """API for Lux Thermostat."""

    def __init__(self, username, password, tokens) -> None:
        """Initialize the API."""
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.username = username
        self.password = password

    async def get_user(self) -> dict:
        """Get the user."""
        url = "https://www.myluxstat.io/api/location/user"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        res, _, _ = await http_request("get", url, headers=headers)
        return json.loads(res)

    async def get_device_state(self, device_id) -> dict:
        """Get the device state."""
        url = "https://www.myluxstat.io/api/device"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Deviceid": device_id,
        }
        res, _, _ = await http_request("get", url, headers=headers)
        return json.loads(res)

    async def set_device_state(self, device_id, state) -> dict:
        """Set the device state."""
        url = "https://www.myluxstat.io/api/device"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Deviceid": device_id,
        }
        res, _, _ = await http_request("put", url, headers=headers, json_data=state)
        return json.loads(res)
