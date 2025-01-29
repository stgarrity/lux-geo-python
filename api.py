import aiohttp
import json

class LuxAPI:

    def __init__(self, tokens):
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]


    async def get_user(self):
        url = "https://www.myluxstat.io/api/location/user"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Authorization": f"Bearer {self.access_token}"}) as response:
                res = await response.text()
                print(res)
                return json.loads(res)


    async def get_device_state(self, device_id):
        url = "https://www.myluxstat.io/api/device"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Authorization": f"Bearer {self.access_token}", "Deviceid": device_id}) as response:
                res = await response.text()
                print(res)
                return json.loads(res)


    async def set_device_state(self, device_id, state):
        url = "https://www.myluxstat.io/api/device"
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers={"Authorization": f"Bearer {self.access_token}", "Deviceid": device_id}, json=state) as response:
                res = await response.text()
                print(res)
                return json.loads(res)
