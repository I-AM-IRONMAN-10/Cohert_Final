# AI-Driven Smart Subscription Commerce Platform

A hackathon-winning, fully-featured subscription box web application. This platform goes beyond a standard e-commerce site by introducing AI-driven personalization, the ability for users to swap items in their box before it ships, loyalty rewards, and a comprehensive admin/staff dashboard.

## Features
- **Smart Recommendation Engine:** Curates monthly items based on a user preference quiz (allergies, favorites).
- **Product Swap Feature:** Users can replace items in their upcoming box before shipment.
- **Flexible Subscriptions:** Users can pause or skip a month instead of cancelling via Razorpay recurring payments.
- **Gift Subscriptions:** Buy 3, 6, or 12-month packages for friends.
- **Loyalty & Referrals:** Earn points per box and per referral; redeem for discounts or extra items.
- **AI Demand Prediction:** The admin dashboard projects inventory required next month based on active user preferences and historical swap behavior.

## Tech Stack
- Frontend: Vanilla HTML, CSS (Modern styling, Glassmorphism), and JavaScript.
- Backend: Python, Flask, MongoEngine
- Database: MongoDB.
- Payments: Razorpay Python SDK.

## How to Run
1. Ensure Python 3.8+ is installed.
2. Create a virtual environment and arrange dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Ensure MongoDB is running locally (or update `.env` with an Atlas URI).
4. Start the backend server: `python backend/app.py` (Runs on `http://localhost:5001`)
5. Serve the frontend folder using a static server (e.g., VS Code Live Server or `npx serve frontend`).

## Authors
Built for hackathon excellence!
