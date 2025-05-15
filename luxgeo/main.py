import asyncio
import json
import os

import dotenv

from api import LuxAPI
from auth import login

dotenv.load_dotenv()

async def main():
    # tokens = await login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    tokens = json.loads(os.getenv("TOKENS"))

    api = LuxAPI(os.getenv("USERNAME"), os.getenv("PASSWORD"), tokens)
    u = await api.get_user()

    device_id = u["location"][0]["devices"][0]["id"]
    print(device_id)
    d = await api.get_device_state(device_id)
    # d["systemmode"] = 0 # 1 for on
    # await api.set_device_state(device_id, d)


if __name__ == "__main__":
    asyncio.run(main())