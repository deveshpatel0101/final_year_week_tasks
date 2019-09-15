import os
from pymongo import MongoClient

client = MongoClient(os.getenv('DB_URL'))
db = client['my_blog']
users = db.users
