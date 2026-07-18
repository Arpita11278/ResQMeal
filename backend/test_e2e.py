import urllib.request
import json
import urllib.error

BASE_URL = "http://localhost:5000"

def test_api(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    if data:
        req.data = json.dumps(data).encode('utf-8')
    try:
        res = urllib.request.urlopen(req)
        body = res.read().decode()
        print(f"[{method}] {endpoint} -> OK")
        return json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[{method}] {endpoint} -> FAILED ({e.code}): {body}")
        return None
    except Exception as e:
        print(f"[{method}] {endpoint} -> FAILED: {e}")
        return None

print("Starting E2E Tests...")

# 1. Users
print("\n--- Users ---")
users = test_api("GET", "/users")
user_id = 1
restaurant_id = 1
ngo_id = 1
if users and len(users) > 0:
    user_id = users[0]['user_id']

# 2. Restaurants
print("\n--- Restaurants ---")
test_api("GET", "/restaurants")
test_api("GET", f"/restaurant/by_user/1")

# 3. NGO
print("\n--- NGO ---")
test_api("GET", f"/ngo/by_user/1")

# 4. Food
print("\n--- Food ---")
test_api("GET", "/food/available")
test_api("GET", f"/food/restaurant/1")

# Try to add a test donation
print("\n--- Donating Food ---")
donation = test_api("POST", "/food/donate", {
    "restaurant_id": 1,
    "food_name": "Test E2E Food",
    "quantity": 5,
    "food_type": "Veg",
    "cooked_at": "2026-07-18 10:00:00",
    "expiry_time": "2026-07-18 20:00:00"
})

# Get available food to find the new ID
available = test_api("GET", "/food/available")
food_id = None
if available and len(available) > 0:
    # get the latest one
    food_id = available[-1]['food_id']
    print(f"Found available food ID: {food_id}")

if food_id:
    # 5. NGO Accept
    print("\n--- NGO Accept ---")
    test_api("POST", "/ngo/accept", {
        "food_id": food_id,
        "ngo_id": 1
    })

    print("\n--- NGO History ---")
    test_api("GET", "/ngo/history/1")

    # 6. Delivery
    print("\n--- Delivery ---")
    tasks = test_api("GET", "/delivery/tasks")
    delivery_id = None
    if tasks and len(tasks) > 0:
        delivery_id = tasks[-1]['delivery_id']
        print(f"Found delivery ID: {delivery_id}")
    
    if delivery_id:
        test_api("POST", "/delivery/assign", {
            "delivery_id": delivery_id,
            "partner_id": 1
        })
        
        test_api("PUT", f"/delivery/update/{delivery_id}", {
            "status": "Picked Up"
        })
        
        test_api("GET", "/delivery/history/1")

print("\nFinished!")
