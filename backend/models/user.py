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