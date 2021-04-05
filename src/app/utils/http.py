import asyncio
import json
import os

import httpx
from fastapi import status
from ..utils.Exceptions import raise_404_exception

from ..api.schemas import User


async def check_user_credentials(user: User):
    URL = os.getenv("CREDENTIALS_URL")
    API_KEY = os.getenv("CREDENTIALS_API_KEY")

    async with httpx.AsyncClient() as client:
        try:
            result = await client.post(url=URL, data=user.json(), headers={"access_token": API_KEY})
            if result.status_code == status.HTTP_200_OK:
                return result.json()
            return False
        except httpx.ConnectError as e:
            print(e)
            raise_404_exception("Users Service Unavailable")

