# from . import User
from fastapi import FastAPI

from .UserRouter import router as user_router


def init(app: FastAPI):
    app.include_router(user_router, tags=["Rec"], prefix="/rec")

    # views = Namespace()
    # views.User = User.User(app)
    # app.state.views=views
