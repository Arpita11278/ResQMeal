def accept_food_donation(mysql, food_id, ngo_id):
    cursor = mysql.connection.cursor()
    # 1. Update the food status from 'Available' to 'Accepted'
    cursor.execute("UPDATE food SET status = 'Accepted' WHERE food_id = %s", (food_id,))
    
    # 2. Insert a record into requests table to track who accepted it
    cursor.execute(
        """
        INSERT INTO requests (food_id, ngo_id, status)
        VALUES (%s, %s, 'Accepted')
        """, (food_id, ngo_id)
    )
    mysql.connection.commit()
    cursor.close()
    return True

def get_ngo_history(mysql, ngo_id):
    cursor = mysql.connection.cursor()
    # Using SQL JOIN to fetch details from 3 tables: requests, food, and restaurants!
    cursor.execute(
        """
        SELECT req.request_id, f.food_name, r.restaurant_name, req.status, req.request_date 
        FROM requests req
        JOIN food f ON req.food_id = f.food_id
        JOIN restaurants r ON f.restaurant_id = r.restaurant_id
        WHERE req.ngo_id = %s
        """, (ngo_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    
    history = []
    for row in rows:
        history.append({
            "request_id": row[0],
            "food_name": row[1],
            "restaurant_name": row[2],
            "status": row[3],
            "request_date": str(row[4])
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
