from typing import Dict
from aiohttp import ClientResponse, ClientSession, ClientTimeout, TCPConnector

from src.main_types import Response


class HttpService:
    def __init__(self):
        self.session = ClientSession(connector=TCPConnector(ssl=False), timeout=ClientTimeout(30))

    async def fetch_html(self, link: str) -> Response:
        async with self.session.get(link) as response:
            return Response(text=await response.text(), headers=response.headers.getall('Set-Cookie'))

    async def post_request(self, link: str, headers: Dict[str, str], data: Dict[str, str]) -> ClientResponse:
        async with self.session.post(link, data=data, headers=headers) as response:
            return response

    async def close_session(self):
        await self.session.close()
