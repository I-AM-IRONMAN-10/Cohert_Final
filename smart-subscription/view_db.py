import sys

def view_db():
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['smart-subscription-ai']
        
        print("\n=== CONNECTED TO MONGODB ===")
        print(f"Database: {db.name}\n")
        
        # USERS
        users = list(db.users.find())
        print(f"--- USERS ({len(users)}) ---")
        for u in users:
            print(f"- Name: {u.get('name')} | Email: {u.get('email')} | Role: {u.get('role', 'user')}")
            
        # PLANS
        plans = list(db.plans.find())
        print(f"\n--- PLANS ({len(plans)}) ---")
        for p in plans:
            print(f"- {p.get('name')} (₹{p.get('price')})")
            
        # INVENTORY
        inventory = list(db.inventories.find())
        print(f"\n--- INVENTORY ({len(inventory)}) ---")
        for i in inventory:
            print(f"- {i.get('productName')} | Qty: {i.get('quantity')}")
            
        # SUBSCRIPTIONS
        subs = list(db.subscriptions.find())
        print(f"\n--- SUBSCRIPTIONS ({len(subs)}) ---")
        for s in subs:
            print(f"- Status: {s.get('status')} | Gift? {s.get('isGift')}")
            
        # ORDERS
        orders = list(db.orders.find())
        print(f"\n--- ORDERS ({len(orders)}) ---")
        for o in orders:
            print(f"- Packing Status: {o.get('packingStatus')} | Track: {o.get('trackingNumber')}")

        print("\n=== END OF DATABASE ===")
        
    except Exception as e:
        print(f"\nFailed to connect or read MongoDB: {e}")

if __name__ == "__main__":
    view_db()