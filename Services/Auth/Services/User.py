from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter

from ..Exceptions.AuthException import LoginExists, AuthDBException, LoginNotExists, PasswordMismatch, \
    TokenInvalid
from ..Models import Responses, User as UserModel
# from ..Models.StateModel import FastAPI_M
from ..Models.FastAPI_helper import FastAPI_M
from ..Models.Responses import Tokens
from ..Services.Utils.DBService import DBService

router = APIRouter()


class User:
    def __init__(self, app):
        self.db_service: DBService = app.state.db_service

        self.app: FastAPI_M = app
        # self.db: pymongo.database.Database = self.db_service.db.get_database(self.db_name)
        # self.coll: pymongo.collection.Collection = self.db.get_collection(self.db_coll)
        # self.DBService = DBService(app.state.config)
        # self.user_dao:UserDAO = app.state.dao.user
        # self.JWT:AuthJwt = app.state.services.JWT


    async def refresh(self, login: str, ref_jwt: str) -> Responses.RefSuccess:
        """

        :raise TokenInvalid:
        :raise TokenExpired:
        :param login:
        :param ref_jwt:
        :return:
        """

        db_user: UserModel.UserIn = await self.app.state.dao.user.get_user_by_login(login)
        if db_user.login is None:
            raise TokenInvalid(f"Refresh token does not belong to user {login}")

        ref_dict = self.app.state.services.JWT.decode_and_validate_ref_token(ref_jwt)

        if db_user.user_id != ref_dict["sub"]:
            raise TokenInvalid(f"Refresh token does not belong to user {login}")

        if ref_jwt not in db_user.jwt_wl:
            raise TokenInvalid("Token was refreshed before. Login ")

        new_tokens = self.app.state.services.JWT.validate_ref_and_refresh_acc_token(ref_jwt)

        ret = Responses.RefSuccess(
                **{
                        "refresh_token": new_tokens.refresh_token,
                        "access_token": new_tokens.access_token,
                        "user_id": db_user.user_id
                })
        await self.app.state.dao.user.reset_ref_jwt(db_user.user_id, new_tokens.refresh_token)

        return ret
