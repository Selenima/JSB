import aiohttp
from typing import Optional, Dict, Any

class BaseAPIClient:

    def __init__(self, base_url: str, api_version: str):
        self.base_url = f'{base_url.rstrip("/")}/{api_version.strip("/")}/'


    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        url = f'{self.base_url}{endpoint.lstrip("/")}'
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                return None

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        return await self._request('GET', endpoint, params=params)

    async def post(self, endpoint: str, params: Optional[Dict] = None, json: Optional[Dict] = None) -> Optional[Dict]:
        return await self._request('POST', endpoint, json=json, params=params)

    async def put(self, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        return await self._request("PUT", endpoint, data=data)

    async def delete(self, endpoint: str) -> Optional[Dict]:
        return await self._request("DELETE", endpoint)

