from fastapi import FastAPI, HTTPException

from src.HTTP_service import HttpService
from src.main_types import UserCredentials
from src.tokens_parser import ParserService
from fake_useragent import UserAgent

app = FastAPI()

GET_URL = 'https://askep.net/login'
POST_URL = 'https://askep.net/doctor/login'

HEADERS = {
    'Host': 'askep.net',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://askep.net/doctor/main-page',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip, deflate'
}


@app.get('/get-cookies')
async def root(login: str, password: str):
    credentials = UserCredentials(login=login, password=password)
    http_service = HttpService()
    try:
        parser = ParserService(http_service=http_service, post_headers=HEADERS)
        response = await parser.get_tokens(credentials=credentials, get_link=GET_URL, post_link=POST_URL)
        return await parser.get_cookies(response.getall('Set-Cookie'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await http_service.close_session()
