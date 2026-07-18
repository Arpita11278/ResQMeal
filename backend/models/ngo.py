def accept_food_donation(mysql, food_id, ngo_id):
    cursor = mysql.connection.cursor()
    # 1. Update the food status from 'Available' to 'Claimed'
    cursor.execute("UPDATE food SET status = 'Claimed' WHERE food_id = %s", (food_id,))
    
    # 2. Create a delivery record
    cursor.execute(
        """
        INSERT INTO deliveries (food_id, ngo_id, pickup_address, drop_address, status)
        SELECT %s, %s, r.address, n.location, 'Pending'
        FROM food f
        JOIN restaurants r ON f.restaurant_id = r.restaurant_id
        JOIN ngo n ON n.ngo_id = %s
        WHERE f.food_id = %s
        """,
        (food_id, ngo_id, ngo_id, food_id)
    )
    mysql.connection.commit()
    cursor.close()
    return True

def get_ngo_history(mysql, ngo_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT d.delivery_id, f.food_name, f.quantity, d.status, p.name as partner_name, d.assigned_at, r.restaurant_name
        FROM deliveries d
        JOIN food f ON d.food_id = f.food_id
        JOIN restaurants r ON f.restaurant_id = r.restaurant_id
        LEFT JOIN users p ON d.partner_id = p.user_id
        WHERE d.ngo_id = %s
    """, (ngo_id,))
    rows = cursor.fetchall()
    cursor.close()
    
    history = []
    for row in rows:
        history.append({
            "delivery_id": row[0],
            "food_name": row[1],
            "quantity": row[2],
            "status": row[3],
            "partner_name": row[4] or "Unassigned",
            "assigned_at": str(row[5]) if row[5] else None,
            "restaurant_name": row[6]
        })
    return history

import MySQLdb

def create_ngo_profile(mysql, data):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO ngo (user_id, ngo_name, capacity, location)
            VALUES (%s, %s, %s, %s)
            """, (data['user_id'], data['ngo_name'], data.get('capacity'), data.get('location'))
        )
        mysql.connection.commit()
        cursor.close()
        return True, None
    except MySQLdb.IntegrityError:
        return False, "This user already has an NGO profile!"
    except Exception as e:
        return False, str(e)

def get_ngo_by_user(mysql, user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT ngo_id, user_id, ngo_name, capacity, location FROM ngo WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    if row:
        return {"ngo_id": row[0], "user_id": row[1], "ngo_name": row[2], "capacity": row[3], "location": row[4]}
    return None
