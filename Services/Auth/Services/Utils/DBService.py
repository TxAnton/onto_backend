import motor.motor_asyncio


class DBService:
    def __init__(self, config):
        self.mongo_url = config.mongo_url
        self.db_name = config.mg_db

    def connect(self):
        # self.db = pymongo.MongoClient(self.mongo_url)
        client: motor.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url)
        self.db: motor.AsyncIOMotorDatabase = client[self.db_name]
