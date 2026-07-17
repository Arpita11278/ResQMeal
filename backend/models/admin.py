def get_all_users(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_id, name, email, role FROM users")
    rows = cursor.fetchall()
    cursor.close()
    
    users = []
    for row in rows:
        users.append({
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[3]
        })
    return users

def delete_user(mysql, user_id):
    cursor = mysql.connection.cursor()
    # Due to CASCADE rules, deleting a user will automatically clean up their profile, food, requests, etc!
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    rows = cursor.rowcount
    cursor.close()
    return rows > 0

def get_analytics(mysql):
    cursor = mysql.connection.cursor()
    analytics = {}
    
    cursor.execute("SELECT COUNT(*) FROM users")
    analytics['total_users'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM food")
    analytics['total_food_donated'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM requests")
    analytics['total_requests_accepted'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM deliveries")
    analytics['total_deliveries'] = cursor.fetchone()[0]
    
    cursor.close()
    return analytics
