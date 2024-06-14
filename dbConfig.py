from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import dotenv_values

config = dotenv_values(".env")


class DBSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, uri=config["MONGODB_URI"], database_name="sample_vector"):
        if not hasattr(self, "_initialized"):  # Initialize only once
            self._initialized = True
            self.client = None
            self.database = None
            self.uri = uri
            self.database_name = database_name
            self.connect()

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.database = self.client[self.database_name]
            print(f"Connected to MongoDB database: {self.database_name}")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")

    def get_database(self):
        try:
            self.client.admin.command("ping")
            return self.database
        except Exception as e:
            self.connect()
            return self.database


mongo_connection = DBSingleton()
mongo_connection.connect()

# db = mongo_connection.get_database()
