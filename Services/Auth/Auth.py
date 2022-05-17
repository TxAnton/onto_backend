from fastapi import FastAPI

from .DAO.init_dao import init as m_init_dao
from .Services.Utils.DBService import DBService
from .Services.init_services import init as m_init_services
from .Views.init_views import init as m_init_views


# from .g_state import g


def init_db(app: FastAPI):
    db_service = DBService(app.state.config)
    db_service.connect()
    app.state.db_service = db_service


def init_services(app: FastAPI):
    m_init_services(app)


def init_views(app):
    m_init_views(app)


def init_dao(app):
    m_init_dao(app)


# _app = None


def create_app(config):
    app = FastAPI()
    app.state.config = config
    init_db(app)
    init_dao(app)
    init_services(app)
    init_views(app)
    # global _app
    # g.app = app

    # _app = app
    return app

#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}
#
#
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"
#
#
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
#
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}
#
#     return {"model_name": model_name, "message": "Have some residuals"}
#
#
# @app.get("/files/{fp1}/{fp2}")
# async def read_file(fp1:str, fp2: str):
#     return {"fp1": fp1,"fp2":fp2}
#
#
