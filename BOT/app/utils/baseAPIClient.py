import aiohttp
from typing import Optional, Dict, Any
from utils import auto_logger


class BaseAPIClient:

    def __init__(self, base_url: str, api_version: str):
        self.base_url = f'{base_url.rstrip("/")}/{api_version.strip("/")}/'


    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        url = f'{self.base_url}{endpoint.lstrip("/")}'
        auto_logger.debug(f'{method} -> {url} :: {kwargs}')
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                auto_logger.debug(f'{method} <- {url} :: {response.status} {await response.text()}')
                return await response.json() if response.status > 199 and response.status < 299 else None


    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        return await self._request('GET', endpoint, params=params)

    async def post(self, endpoint: str, params: Optional[Dict] = None, json: Optional[Dict] = None) -> Optional[Dict]:
        return await self._request('POST', endpoint, json=json, params=params)

    async def put(self, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        return await self._request("PUT", endpoint, data=data)

    async def delete(self, endpoint: str) -> Optional[Dict]:
        return await self._request("DELETE", endpoint)

