import aiohttp
import asyncio
import urllib.parse
import json
from .const import HTTP_HEADERS, HTTP_API_URL

class Client:
    def __init__(self):
        if not hasattr(type(self), '_session'):
            self._create_session()

    @classmethod
    def _create_session(cls):
        cls._session = aiohttp.ClientSession(headers=HTTP_HEADERS)

    async def authenticate(self, hass, email: str, password: str, token: str):
        auth_url = f'{HTTP_API_URL}/apihelper/UserLogin?clientOS=ios&notifyService=APNs&password={password}&token={token}&username={urllib.parse.quote_plus(email)}'
        async with self._session.get(auth_url) as auth:
          return await auth.json()

    async def values(self):
        data_url = f'{HTTP_API_URL}/resources/user/data'
        async with self._session.get(data_url) as data:
          body = await data.json()
          return body["response"]["meterPoints"][0]["lastMeasurements"]
