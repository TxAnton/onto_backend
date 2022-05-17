from Auth import Auth
from config import get_config

# if __name__ == "__main__":
cfg = get_config()
app = Auth.create_app(cfg)

# print(app)
# app.rt = Namespace()
# app = FastAPI()

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
