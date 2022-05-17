from typing import Dict, Optional

import motor.core
import pymongo
from bson import ObjectId
from fastapi import FastAPI

# from ..Models.User import UserDBInModel, UserDBOutModel
from ..Services.Utils.DBService import DBService


class UserDAO:
    def __init__(self, app: FastAPI):
        self.db_service: DBService = app.state.db_service
        self.db_name = app.state.config.mg_db
        self.db_coll = app.state.config.mg_coll
        self.db: motor.core.AgnosticDatabase = self.db_service.db
        # self.coll: pymongo.collection.Collection = self.db.get_collection(self.db_coll)
        self.ref: pymongo.collection.Collection = None
        # ref

    async def get_user_by_login(self, login: str) -> Optional[UserDBOutModel]:
        db_user = await self.db.get_collection(self.db_coll).find_one({'login': login})
        if not db_user:
            return None
        return self._db_user_to_out_model(db_user)

    def _db_user_to_out_model(self, db_user: Dict) -> UserDBOutModel:
        db_user.update({"user_id": str(db_user["_id"])})
        cons_user: UserDBOutModel = UserDBOutModel.parse_obj(db_user)
        return cons_user

    async def reserve_user(self) -> ObjectId:
        res = await self.db[self.db_coll].insert_one({})
        return res.inserted_id

    async def create_reserved(self, user_id: str, user: UserDBInModel):
        res = await self.db.get_collection(self.db_coll).update_one({"_id": ObjectId(user_id)},
                                                                    {"$set": user.dict()})
        return bool(res.modified_count)

    async def unreserve_user(self, user_id: str):  # TODO check if slot is reserved, not real user
        res = await self.db.get_collection(self.db_coll).delete_one({"_id": ObjectId(user_id)})

    async def reset_ref_jwt(self, user_id: str, new_ref_jwt: Optional[str]) -> None:
        user_id = ObjectId(user_id)
        res = await self.db.get_collection(self.db_coll).update_one({"_id": user_id},
                                                                    {"$set": {"jwt_wl": []}})
        if new_ref_jwt is not None:
            await self.db.get_collection(self.db_coll).update_one({"_id": user_id},
                                                                  {"$push": {"jwt_wl": new_ref_jwt}})
