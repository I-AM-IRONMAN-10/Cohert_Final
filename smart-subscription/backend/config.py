import os
from dotenv import load_dotenv
from mongoengine import connect
import razorpay

load_dotenv()

class Config:
    PORT = int(os.environ.get('PORT', 5001))
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/smart-subscription-ai')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'super_secret_jwt_key_here')
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'YOUR_RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'YOUR_RAZORPAY_KEY_SECRET')
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5500')

def connect_db():
    connect(host=Config.MONGO_URI)
    print("MongoDB Connected via MongoEngine")

# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))
