def assign_delivery(mysql, data):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        INSERT INTO deliveries (request_id, partner_id, status)
        VALUES (%s, %s, 'Assigned')
        """, (data['request_id'], data['partner_id'])
    )
    mysql.connection.commit()
    cursor.close()
    return True

def update_delivery_status(mysql, delivery_id, status, time_field, time_value):
    cursor = mysql.connection.cursor()
    # Dynamically update either pickup_time or delivery_time based on status
    query = f"UPDATE deliveries SET status = %s, {time_field} = %s WHERE delivery_id = %s"
    cursor.execute(query, (status, time_value, delivery_id))
    mysql.connection.commit()
    rows = cursor.rowcount
    cursor.close()
    return rows > 0

def get_delivery_tasks(mysql, partner_id):
    cursor = mysql.connection.cursor()
    # Complex JOIN query to provide full delivery details to the Delivery Partner
    cursor.execute(
        """
        SELECT 
            d.delivery_id, 
            f.food_name, 
            rest.restaurant_name, rest.address AS pickup_address, rest.phone AS pickup_phone,
            n.ngo_name, n.location AS drop_address,
            d.status
        FROM deliveries d
        JOIN requests req ON d.request_id = req.request_id
        JOIN food f ON req.food_id = f.food_id
        JOIN restaurants rest ON f.restaurant_id = rest.restaurant_id
        JOIN ngo n ON req.ngo_id = n.ngo_id
        WHERE d.partner_id = %s
        """, (partner_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    
    tasks = []
    for row in rows:
        tasks.append({
            "delivery_id": row[0],
            "food_name": row[1],
            "pickup_from": row[2],
            "pickup_address": row[3],
            "pickup_phone": row[4],
            "drop_to": row[5],
            "drop_address": row[6],
            "status": row[7]
        })
    return tasks
