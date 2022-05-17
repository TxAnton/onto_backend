from argparse import Namespace

from fastapi import FastAPI

from .NeoDAO import NeoDAO
# from .UserDAO import UserDAO


def init(app: FastAPI):
    dao = Namespace()
    # dao.user = UserDAO(app)
    dao.neo = NeoDAO(app)
    app.state.dao = dao
