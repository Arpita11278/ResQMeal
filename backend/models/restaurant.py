import MySQLdb

def create_restaurant_profile(mysql, data):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO restaurants 
            (user_id, restaurant_name, owner_name, phone, address, city, opening_time, closing_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (data['user_id'], data['restaurant_name'], data['owner_name'], data['phone'], 
             data['address'], data['city'], data['opening_time'], data['closing_time'])
        )
        mysql.connection.commit()
        cursor.close()
        return True, None
    except MySQLdb.IntegrityError:
        return False, "This user already has a restaurant profile!"

def get_restaurant_by_id(mysql, restaurant_id):
    cursor = mysql.connection.cursor()
    # Updated to match the user's existing DB schema which uses `restaurant_id` instead of `id`
    cursor.execute("""
        SELECT restaurant_id, user_id, restaurant_name, owner_name, phone, address, city, opening_time, closing_time 
        FROM restaurants WHERE restaurant_id=%s
    """, (restaurant_id,))
    
    row = cursor.fetchone()
    cursor.close()
    
    if row:
        return {
            "restaurant_id": row[0],
            "user_id": row[1],
            "restaurant_name": row[2],
            "owner_name": row[3],
            "phone": row[4],
            "address": row[5],
            "city": row[6],
            "opening_time": row[7],
            "closing_time": row[8]
        }
    return None

def update_restaurant_profile(mysql, restaurant_id, data):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        UPDATE restaurants 
        SET restaurant_name=%s, owner_name=%s, phone=%s, address=%s, city=%s, opening_time=%s, closing_time=%s
        WHERE restaurant_id=%s
        """,
        (data['restaurant_name'], data['owner_name'], data['phone'], data['address'], 
         data['city'], data['opening_time'], data['closing_time'], restaurant_id)
    )
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected > 0

def get_all_restaurants(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT restaurant_id, user_id, restaurant_name, owner_name, phone, address, city, opening_time, closing_time 
        FROM restaurants
    """)
    rows = cursor.fetchall()
    cursor.close()
    
    restaurants = []
    for row in rows:
        restaurants.append({
            "restaurant_id": row[0],
            "user_id": row[1],
            "restaurant_name": row[2],
            "owner_name": row[3],
            "phone": row[4],
            "address": row[5],
            "city": row[6],
            "opening_time": row[7],
            "closing_time": row[8]
        })
    return restaurants