import asyncio
import json
import os

import httpx

from ..api.schemas import User


async def check_user_credentials(user: User):
    URL = os.getenv("CREDENTIALS_URL")
    API_KEY = os.getenv("CREDENTIALS_API_KEY")

    async with httpx.AsyncClient() as client:
        result = await client.post(url=URL, data=user.json(), headers={"access_token": API_KEY})
        return result.status_code
