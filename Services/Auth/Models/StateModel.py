from fastapi import FastAPI
from pydantic import BaseModel

from .Config import Config as ConfigModel
from ..DAO.NeoDAO import NeoDAO
# from ..DAO.UserDAO import UserDAO
from ..Services.User import User as UserService
from ..Services.Utils.DBService import DBService
from ..Services.Utils.Jwt import AuthJwt


# from typing import TYPE_CHECKING

# from .. import DAO as _DAO


class Services(BaseModel):
    user: UserService
    JWT: AuthJwt
    db_service: DBService

    class Config:
        arbitrary_types_allowed = True


class DAO(BaseModel):
    # user: UserDAO
    neo: NeoDAO

    class Config:
        arbitrary_types_allowed = True


class State(BaseModel):
    services: Services
    dao: DAO
    config: ConfigModel

    class Config:
        arbitrary_types_allowed = True


class FastAPI_M(FastAPI):
    state: State
