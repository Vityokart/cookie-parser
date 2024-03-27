from typing import Dict

from aiohttp import ClientConnectionError
from bs4 import BeautifulSoup

from src.HTTP_service import HttpService
from src.main_types import Tokens, ClientType, RequestToken, UserCredentials

CLIENT_TYPE = ClientType(client_type='doctor')


class ParserService:
    def __init__(self, http_service: HttpService, post_headers: Dict[str, str]):
        self.http_service = http_service
        self.post_headers = post_headers

    @staticmethod
    async def get_cookies(response: list[str]) -> Dict[str, str]:
        cookies = {}
        for cookie_header in response:
            splited_cookies = cookie_header.split('=')
            key = splited_cookies[0]
            value = splited_cookies[1].split(';')[0]
            cookies[key] = value
        return cookies

    @staticmethod
    async def parse_tokens(html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        token_input = soup.find('input', attrs={"name": "_token"})
        token = token_input.get("value")
        return token

    async def get_user_data(self, link: str) -> Tokens:
        try:
            response = await self.http_service.fetch_html(link=link)
            headers = response.headers
            html = response.text
            token: str = await self.parse_tokens(html)
            request_cookies: Dict[str, str] = await self.get_cookies(headers)
            xsrf_token: str = list(request_cookies.values())[0]
            laravel_session: str = list(request_cookies.values())[1]

            return Tokens(token=token, xsrf_token=xsrf_token, laravel_session=laravel_session)
        except ClientConnectionError:
            raise ConnectionError

    async def get_headers(self, tokens: RequestToken) -> Dict[str, str]:
        self.post_headers.__setitem__("Cookie",
                                      f"XSRF-TOKEN={tokens.xsrf_token}; laravel_session={tokens.laravel_session};")
        return self.post_headers

    async def get_tokens(self, credentials: UserCredentials, get_link: str, post_link: str):
        tokens = await self.get_user_data(get_link)

        postData = {"_token": tokens.token, "client-type": CLIENT_TYPE.client_type, "username": credentials.login,
                    "password": credentials.password}

        headers: Dict[str, str] = await self.get_headers(
            tokens=RequestToken(xsrf_token=tokens.xsrf_token, laravel_session=tokens.laravel_session))

        response = await self.http_service.post_request(link=post_link, headers=headers, data=postData)
        return response.headers
