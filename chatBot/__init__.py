from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dbConfig import DBSingleton

# from dotenv import dotenv_values

# config = dotenv_values(".env")

# client = MongoClient(config["MONGODB_URI"], server_api=ServerApi("1"))

# try:
#     global db

#     client.admin.command("ping")
#     db = client.sample_vector

#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
