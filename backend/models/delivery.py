def assign_delivery(mysql, data):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        UPDATE deliveries
        SET partner_id = %s, status = 'Assigned', assigned_at = NOW()
        WHERE delivery_id = %s
        """, (data['partner_id'], data['delivery_id'])
    )
    mysql.connection.commit()
    cursor.close()
    return True

def update_delivery_status(mysql, delivery_id, status, time_field, time_value):
    cursor = mysql.connection.cursor()
    # In Clever Cloud schema, we don't have pickup_time or delivery_time columns, only assigned_at.
    # So we'll just update the status for now.
    query = "UPDATE deliveries SET status = %s WHERE delivery_id = %s"
    cursor.execute(query, (status, delivery_id))
    mysql.connection.commit()
    rows = cursor.rowcount
    cursor.close()
    return rows > 0

def get_available_deliveries(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT 
            d.delivery_id, 
            f.food_name, 
            rest.restaurant_name, rest.address AS pickup_address, rest.phone AS pickup_phone,
            n.ngo_name, n.location AS drop_address,
            d.status
        FROM deliveries d
        JOIN food f ON d.food_id = f.food_id
        JOIN restaurants rest ON f.restaurant_id = rest.restaurant_id
        JOIN ngo n ON d.ngo_id = n.ngo_id
        WHERE d.partner_id IS NULL AND d.status = 'Pending'
        """
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

def get_delivery_tasks(mysql, partner_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        """
        SELECT 
            d.delivery_id, 
            f.food_name, 
            rest.restaurant_name, rest.address AS pickup_address, rest.phone AS pickup_phone,
            n.ngo_name, n.location AS drop_address,
            d.status
        FROM deliveries d
        JOIN food f ON d.food_id = f.food_id
        JOIN restaurants rest ON f.restaurant_id = rest.restaurant_id
        JOIN ngo n ON d.ngo_id = n.ngo_id
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
