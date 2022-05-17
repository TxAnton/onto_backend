import typing
from typing import TYPE_CHECKING

from fastapi import FastAPI

FastAPI_M = typing.Any
if TYPE_CHECKING:
    from . import StateModel

    FastAPI_M = StateModel.FastAPI_M
else:
    FastAPI_M = FastAPI
