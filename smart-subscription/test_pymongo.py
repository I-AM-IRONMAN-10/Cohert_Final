from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['smart-subscription-ai']
users = db.users.find()
print("PyMongo Connection successful!")
count = 0
for u in users:
    print(u)
    count += 1
print(f"Total users: {count}")
