import sys
from mongoengine import connect
from models.User import User
from pprint import pprint

try:
    connect(host='mongodb://localhost:27017/smart-subscription-ai')
    users = User.objects()
    print(f"Connection successful!")
    print(f"Total users found: {users.count()}")
    for user in users:
        print(f" - {user.name} ({user.email})")
except Exception as e:
    print(f"Connection failed: {e}")
