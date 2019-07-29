import sqlite3

import pymongo

from conf.base import MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DATABASE

client = pymongo.MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}")
db_reptile = client[MONGO_DATABASE]


# sqlite_connect = sqlite3.connect(download_sql_path)
# sqlite_cursor = sqlite_connect.cursor()
