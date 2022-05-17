from typing import Optional, List

from email_validator import EmailNotValidError
from fastapi import Request, APIRouter, Query
from starlette.responses import JSONResponse

from ..Exceptions.AuthException import LoginExists, LoginNotExists, PasswordMismatch, \
    TokenInvalid, TokenExpired
from ..Models import User as UserModel, Responses
from ..Models.FastAPI_helper import FastAPI_M

router = APIRouter()


@router.post("/hello", status_code=201,
             responses={400: {"model": Responses.Error}, 520: {"model": Responses.Error}})
async def reg_user(req: Request):
    app: FastAPI_M = req.app
    try:
        res: Responses.RegSuccess = await app.state.dao.neo.hello_world()
    except Exception as e:
        return e
    else:
        return res

## THING

@router.get("/things", status_code=200, tags=['thing'])
async def get_things(req: Request, restrict_types:List[str]= Query(None), offset: int = 0, limit: int = 100):
    app: FastAPI_M = req.app
    config = app.state.config

@router.get("/things/professions", status_code=200, tags=['thing'])
async def get_professions(req: Request, offset: int = 0, limit: int = 100):
    app: FastAPI_M = req.app
    config = app.state.config


@router.get("/things/find", status_code=200, tags=['thing'])
async def find_things(req: Request, query: str, restrict_types:Optional[List[str]]= Query(None), offset: int = 0, limit: int = 100):
    app: FastAPI_M = req.app
    config = app.state.config
    # return str(req)

## USER

@router.get("/user/list", status_code=200,tags=['user'])
async def get_users(req: Request, offset: int = 0, limit: int = 100):
    app: FastAPI_M = req.app
    config = app.state.config

@router.get("/user/{user_id}", status_code=200,tags=['user'])
async def get_user(req: Request, user_id:int):
    app: FastAPI_M = req.app
    config = app.state.config

@router.post("/user/", status_code=200,tags=['user'])
async def create_user(req: Request, user: UserModel.UserIn):
    app: FastAPI_M = req.app
    config = app.state.config

@router.put("/user/", status_code=200,tags=['user'])
async def change_user(req: Request, user: UserModel.UserIn, ):
    app: FastAPI_M = req.app
    config = app.state.config

@router.delete("/user/{user_id}", status_code=200,tags=['user'])
async def change_user(req: Request, user_id:int):
    app: FastAPI_M = req.app
    config = app.state.config

## PROJECT

@router.get("/project/list", status_code=200,tags=['project'])
async def get_projects(req: Request, offset: int = 0, limit: int = 100):
    app: FastAPI_M = req.app
    config = app.state.config

@router.get("/project/{project_id}", status_code=200,tags=['project'])
async def get_project(req: Request, project_id:int):
    app: FastAPI_M = req.app
    config = app.state.config

@router.post("/project/", status_code=200,tags=['project'])
async def create_project(req: Request, project: UserModel.ProjectIn):
    app: FastAPI_M = req.app
    config = app.state.config

@router.put("/project/", status_code=200,tags=['project'])
async def change_project(req: Request, project: UserModel.ProjectIn):
    app: FastAPI_M = req.app
    config = app.state.config

@router.delete("/project/{project_id}", status_code=200,tags=['project'])
async def change_user(req: Request, project_id:int):
    app: FastAPI_M = req.app
    config = app.state.config

## FUNCS

@router.get("/metric/{ent_a}/{ent_b}", status_code=200,tags=['metric'])
async def get_dist_ent_ent(req: Request, ent_a:str,ent_b:str):
    app: FastAPI_M = req.app
    config = app.state.config


#
#
# @router.post("/user/", status_code=200,tags=['user'])
# async def get_users(req: Request, user: UserModel.UserIn):
#     app: FastAPI_M = req.app
#     config = app.state.config


@router.post("/register", status_code=201, response_model=Responses.RegSuccess,
             responses={400: {"model": Responses.Error}, 520: {"model": Responses.Error}})
async def reg_user(user: UserModel.UserIn, req: Request):
    app: FastAPI_M = req.app
    try:
        reg_res: Responses.RegSuccess = await app.state.services.user.create(user)
    except LoginExists as e:
        return JSONResponse(status_code=400, content={"err_msg": str(e) or f"Login is taken"})
    except EmailNotValidError as e:
        return JSONResponse(status_code=400, content={"err_msg": str(e) or f"Email is not valid"})
    # except (AuthDBException, Exception) as e:
    #     return JSONResponse(status_code=520, content={"err_msg": str(e) or f"Unknown error"})
    else:
        return reg_res


@router.post("/login", status_code=200, response_model=Responses.LoginSuccess,
             responses={403: {"model": Responses.Error}})
async def login(user: UserModel.UserIn, req: Request):
    # TODO send email to validate
    app: FastAPI_M = req.app
    try:
        login_res: Responses.LoginSuccess = await app.state.services.user.login(user)
    except LoginNotExists as e:
        return JSONResponse(status_code=403, content={"err_msg": f"Wrong login of password"})
    except PasswordMismatch as e:
        return JSONResponse(status_code=403, content={"err_msg": f"Wrong login of password"})
    # except Exception as e:
    #     return JSONResponse(status_code=520, content={"err_msg": str(e) or f"Unknown error"})
    else:
        return login_res


@router.post("/decode_jwt", status_code=200, response_model=Responses.JWTDecode)
async def decode(jwt: str, req: Request):
    app: FastAPI_M = req.app
    return app.state.services.JWT.decode_and_validate_any(jwt)


@router.post("/refresh", status_code=200, response_model=Responses.RefSuccess)
async def refresh(login: str, ref_jwt: str, req: Request):
    app: FastAPI_M = req.app
    try:
        ret = await app.state.services.user.refresh(login=login, ref_jwt=ref_jwt)
    except TokenInvalid as e:
        return JSONResponse(status_code=403, content={"err_msg": str(e) or f"Token or login invalid"})
    except TokenExpired as e:
        return JSONResponse(status_code=403, content={"err_msg": str(e) or f"Token expired"})
    else:
        return ret
