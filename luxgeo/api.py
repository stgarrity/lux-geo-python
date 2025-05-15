"""API for Lux Thermostat."""

import json
from auth import login
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
        res, _, _ = await self._make_request("get", url, headers=headers)
        return json.loads(res)

    async def get_device_state(self, device_id) -> dict:
        """Get the device state."""
        url = "https://www.myluxstat.io/api/device"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Deviceid": device_id,
        }
        res, _, _ = await self._make_request("get", url, headers=headers)
        print(res)
        return json.loads(res)

    async def set_device_state(self, device_id, state) -> dict:
        """Set the device state."""
        url = "https://www.myluxstat.io/api/device"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Deviceid": device_id,
        }
        res, _, _ = await self._make_request("put", url, headers=headers, json_data=state)
        return json.loads(res)

    async def _make_request(self, method, url, headers, data=None, json_data=None):
        res, _, _ = await http_request(method, url, headers=headers, data=data, json_data=json_data)
        j = json.loads(res)
        if "statusCode" in j and j["statusCode"] == 401:
            tokens = await login(self.username, self.password)
            print("here", tokens)
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            headers["Authorization"] = f"Bearer {self.access_token}"
            return await http_request(method, url, headers, json_data=json_data)
        return res, None, None # return res here instead of j because we already decode in the caller
