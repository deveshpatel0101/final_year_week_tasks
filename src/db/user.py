from pymongo import MongoClient

client = MongoClient()
db = client['my_blog']
users = db.users
