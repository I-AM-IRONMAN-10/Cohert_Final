from config import connect_db
from models.User import User
import sys
import os

try:
    print(f"Connecting to {os.environ.get('MONGO_URI', 'mongodb://localhost:27017/smart-subscription-ai')}")
    connect_db()
    users = User.objects()
    print("Users connection successful")
except Exception as e:
    print(f"Error: {e}")
