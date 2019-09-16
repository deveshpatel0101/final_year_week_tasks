import os
from pymongo import MongoClient

client = MongoClient(os.getenv('DB_URL'))
db = client[os.getenv('DB_NAME') or 'my_blog']
users = db[os.getenv('DB_COLLECTION_NAME') or 'users']
