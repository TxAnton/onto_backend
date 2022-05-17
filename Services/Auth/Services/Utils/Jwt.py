import time
from typing import Dict, List

# from . import _config as Config
# from config import Config
# import connexion
from bson import ObjectId
from jose import jwt

# from werkzeug.exceptions import Unauthorized
from ...Exceptions.AuthException import TokenExpired, TokenInvalid
from ...Models.Config import Config
from ...Models.Responses import JWTDecode, JWTToken, Tokens


class AuthJwt:
    def __init__(self, config):
        self.config: Config = config

    # from .runtime import config as Config

    def generate_access_token(self, payload: Dict):
        timestamp = _current_timestamp()
        _payload = {
                "iss": self.config.jwt_issuer,
                "iat": int(timestamp),
                "exp": int(timestamp + self.config.jwt_acc_lifetime_seconds),
                "scope": "access",
                "sub": "default",
        }
        _payload.update(payload)

        return jwt.encode(_payload, self.config.jwt_secret, algorithm=self.config.jwt_algorithm, )

    def generate_refresh_token(self, payload: Dict):
        timestamp = _current_timestamp()
        _payload = {
                "iss": self.config.jwt_issuer,
                "iat": int(timestamp),
                "exp": int(timestamp + self.config.jwt_ref_lifetime_seconds),
                "scope": "refresh",
                "sub": "default",
        }
        _payload.update(payload)

        return jwt.encode(_payload, self.config.jwt_secret, algorithm=self.config.jwt_algorithm, )

    def decode_and_validate_acc_token(self, acc_jwt: str) -> Dict:
        """
        :raise TokenInvalid:
        :raise TokenExpired:
        :param acc_jwt:
        :return jwt_dict:
        """
        try:
            acc_dict = self.decode_token(acc_jwt)
        # except JWTError:
        except:
            raise TokenInvalid()

        if acc_dict["scope"] != 'access':
            raise TokenInvalid(f'Wrong scope. Expected :\'access\', got:\'{acc_dict["scope"]}\'')

        if acc_dict["exp"] <= _current_timestamp():
            raise TokenExpired("Access token expired")

        if not self._validate_user_id(acc_dict["sub"]):
            raise TokenInvalid(f'Invalid user_id: \'{acc_dict["sub"]}\'')
        return acc_dict

    def decode_and_validate_ref_token(self, ref_jwt: str) -> Dict:
        """
        :raise TokenInvalid:
        :raise TokenExpired:
        :param ref_jwt:
        :return jwt_dict:
        """
        try:
            ref_dict = self.decode_token(ref_jwt)
        # except JWTError:
        except:
            raise TokenInvalid()

        if ref_dict["scope"] != 'refresh':
            raise TokenInvalid(f'Wrong scope. Expected :\'refresh\', got:\'{ref_dict["scope"]}\'')

        if ref_dict["exp"] <= _current_timestamp():
            raise TokenExpired("Refresh token expired.")

        if not self._validate_user_id(ref_dict["sub"]):
            raise TokenInvalid(f'Invalid user_id: \'{ref_dict["sub"]}\'')
        return ref_dict

    def decode_and_validate_any(self, jwt) -> JWTDecode:
        """
        :raise None:
        :param jwt:
        :return:
        """
        errs: List[str] = []
        try:
            jwt_dict = self.decode_token(jwt)
        # except JWTError:
        except:
            errs.append("Failed to decode token")
            return JWTDecode(**{"status": "Invalid", "token": None, "errors": errs})

        if jwt_dict["exp"] <= _current_timestamp():
            errs.append("Token expired.")

        if not self._validate_user_id(jwt_dict["sub"]):
            errs.append(f'Invalid user_id: \'{jwt_dict["sub"]}\'')

        if not jwt_dict.get("scope") or (
                jwt_dict.get("scope") != 'refresh' and jwt_dict.get("scope") != 'access'):
            errs.append(f'Bad or missing scope')
        if jwt_dict and not errs:
            status = "Valid"
        else:
            status = "Invalid"

        token = JWTToken(**jwt_dict)
        resp = JWTDecode(
                **{
                        "status": status,
                        "errors": errs,
                        "token": token
                }
        )

        return resp

    def validate_ref_and_refresh_acc_token(self, ref_jwt: str) -> Tokens:
        """

        :raise TokenInvalid:
        :raise TokenExpired:
        :param ref_jwt:
        :return:
        """
        ref_dict = self.decode_and_validate_ref_token(ref_jwt)

        new_acc_jwt = self.generate_access_token({"sub": ref_dict["sub"]})
        new_ref_jwt = self.generate_refresh_token({"sub": ref_dict["sub"]})
        return Tokens(refresh_token=new_ref_jwt, access_token=new_acc_jwt)

    def _validate_user_id(self, user_id: str):
        try:
            u = ObjectId(user_id)
            return True
        except:
            return False

    def decode_token(self, token):
        return jwt.decode(token, self.config.jwt_secret, algorithms=[self.config.jwt_algorithm])

    def md5password(self, password: str):
        return md5(password)


def _current_timestamp() -> int:
    return int(time.time())


def md5(str_: str) -> str:  # 32 bytes
    import hashlib
    return hashlib.md5(str_.encode('utf-8')).hexdigest()
