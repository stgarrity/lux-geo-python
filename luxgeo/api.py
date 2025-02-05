"""API for Lux Thermostat."""

import json

import aiohttp


class LuxAPI:
    """API for Lux Thermostat."""

    def __init__(self, tokens) -> None:
        """Initialize the API."""
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]

    async def get_user(self) -> dict:
        """Get the user."""
        url = "https://www.myluxstat.io/api/location/user"
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                url, headers={"Authorization": f"Bearer {self.access_token}"}
            ) as response,
        ):
            res = await response.text()
            return json.loads(res)

    async def get_device_state(self, device_id) -> dict:
        """Get the device state."""
        url = "https://www.myluxstat.io/api/device"
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                url,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Deviceid": device_id,
                },
            ) as response,
        ):
            res = await response.text()
            return json.loads(res)

    async def set_device_state(self, device_id, state) -> dict:
        """Set the device state."""
        url = "https://www.myluxstat.io/api/device"
        async with (
            aiohttp.ClientSession() as session,
            session.put(
                url,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Deviceid": device_id,
                },
                json=state,
            ) as response,
        ):
            res = await response.text()
            return json.loads(res)
