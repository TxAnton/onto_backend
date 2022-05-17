from pydantic import BaseSettings


class Config(BaseSettings):
    debug: str = True
    secret_key: str
    md5_salt: str
    jwt_issuer: str
    jwt_secret: str
    jwt_acc_lifetime_seconds: int
    jwt_ref_lifetime_seconds: int
    jwt_algorithm: str
    mongo_url: str
    mg_db: str
    mg_coll: str
    neo_url: str
    neo_user: str
    neo_pwd: str
    neo_timeout: int
