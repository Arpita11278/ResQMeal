def donate_food(mysql, data):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO food (restaurant_id, food_name, quantity, food_type, cooked_at, expiry_time, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Available')
        """,
        (data['restaurant_id'], data['food_name'], data['quantity'], data['food_type'], data['cooked_at'], data['expiry_time'])
    )
    mysql.connection.commit()
    cursor.close()
    return True

def get_available_food(mysql):
    cursor = mysql.connection.cursor()
    # JOIN with restaurants table to get the restaurant name
    cursor.execute(
        """
        SELECT f.food_id, f.restaurant_id, r.restaurant_name, f.food_name, f.quantity, f.food_type, f.cooked_at, f.expiry_time, f.status 
        FROM food f
        JOIN restaurants r ON f.restaurant_id = r.restaurant_id
        WHERE f.status = 'Available'
        """
    )
    rows = cursor.fetchall()
    cursor.close()
    
    food_list = []
    for row in rows:
        food_list.append({
            "food_id": row[0],
            "restaurant_id": row[1],
            "restaurant_name": row[2],
            "food_name": row[3],
            "quantity": row[4],
            "food_type": row[5],
            "cooked_at": str(row[6]),
            "expiry_time": str(row[7]),
            "status": row[8]
        })
    return food_list

def update_food(mysql, food_id, data):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        UPDATE food 
        SET food_name=%s, quantity=%s, food_type=%s, cooked_at=%s, expiry_time=%s
        WHERE food_id=%s
        """,
        (data['food_name'], data['quantity'], data['food_type'], data['cooked_at'], data['expiry_time'], food_id)
    )
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected > 0

def delete_food(mysql, food_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM food WHERE food_id=%s", (food_id,))
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected > 0
