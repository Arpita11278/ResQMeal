def create_user(mysql, name, email, password, role):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        return {"message": "Email already exists"}

    cursor.execute(
        """
        INSERT INTO users(name,email,password,role)
        VALUES(%s,%s,%s,%s)
        """,
        (name, email, password, role)
    )

    mysql.connection.commit()

    cursor.close()

    return {"message": "User Registered Successfully"}

def verify_user(mysql, email, password):
    cursor = mysql.connection.cursor()
    
    # Check if a user with this email and password exists
    cursor.execute(
        "SELECT user_id, name, role FROM users WHERE email=%s AND password=%s",
        (email, password)
    )
    
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        return {"user_id": user[0], "name": user[1], "role": user[2]}
    return None