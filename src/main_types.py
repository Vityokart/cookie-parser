from dataclasses import dataclass


@dataclass
class UserCredentials:
    login: str
    password: str


@dataclass
class RequestToken:
    xsrf_token: str
    laravel_session: str


@dataclass
class Tokens(RequestToken):
    token: str


@dataclass
class ClientType:
    client_type: str


@dataclass
class Response:
    text: str
    headers: list[str]
