from functools import lru_cache

from Auth.Models.Config import Config


class Settings(Config):
    class Config:
        env_file = ".env"


# class Settings(BaseSettings):
#     debug: str = True
#     secret_key: str
#     md5_salt: str
#     jwt_issuer: str
#     jwt_secret: str
#     jwt_lifetime_seconds: int
#     jwt_algorithm: str
#     mongo_url: str
#     mg_db:str
#     mg_coll:str
#
#     class Config:
#         env_file = ".env"

@lru_cache()
def get_config() -> Settings:
    return Settings()
