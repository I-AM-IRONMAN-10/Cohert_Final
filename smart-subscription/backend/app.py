from flask import Flask, jsonify
from flask_cors import CORS
from config import connect_db, Config

# Initialize Database
connect_db()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Smart Subscription API is running (Python Flask)..."})

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.plan_routes import plan_bp
from routes.subscription_routes import subscription_bp
from routes.order_routes import order_bp
from routes.reward_routes import reward_bp
from routes.admin_routes import admin_bp
from routes.staff_routes import staff_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(plan_bp, url_prefix='/api/plans')
app.register_blueprint(subscription_bp, url_prefix='/api/subscriptions')
app.register_blueprint(order_bp, url_prefix='/api/orders')
app.register_blueprint(reward_bp, url_prefix='/api/rewards')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(staff_bp, url_prefix='/api/staff')

if __name__ == '__main__':
    print(f"Server running in development mode on port {Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
