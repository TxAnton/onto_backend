from argparse import Namespace

from fastapi import FastAPI

from .User import User
from .Utils import Jwt


def init(app: FastAPI):
    services = Namespace()
    app.state.services = services
    app.state.services.JWT = Jwt.AuthJwt(app.state.config)
    app.state.services.user = User(app)
