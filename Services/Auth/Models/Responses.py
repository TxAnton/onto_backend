from typing import List, Optional

from pydantic import BaseModel


class Tokens(BaseModel):
    refresh_token: str
    access_token: str


class AuthSuccess(Tokens):
    status: str = "Success"
    user_id: str


class RegSuccess(AuthSuccess):
    status: str = "Registered successfully"


class RefSuccess(AuthSuccess):
    status: str = "Refreshed successfully"


class LoginSuccess(AuthSuccess):
    status: str = "Logged in successfully"


class JWTToken(BaseModel):
    iss: str
    iat: int
    exp: int
    scope: str
    sub: str

    class Config:
        extra = "allow"


class JWTDecode(BaseModel):
    status: str
    errors: List[str] = []
    token: Optional[JWTToken]

    class Config:
        arbitrary_types_allowed = True


class Error(BaseModel):
    err_msg: str
