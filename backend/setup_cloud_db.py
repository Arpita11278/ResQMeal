import MySQLdb

try:
    print("Connecting to Clever Cloud MySQL...")
    db = MySQLdb.connect(
        host="b2nefrhzgt6s5ik2rufs-mysql.services.clever-cloud.com",
        user="u90mrcwewzpcp7wq",
        passwd="0oHIIMEfeUMH0w8V6jOg",
        db="b2nefrhzgt6s5ik2rufs",
        port=3306
    )
    cursor = db.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('Restaurant', 'NGO', 'Delivery', 'Admin') NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS restaurants (
            restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            restaurant_name VARCHAR(255) NOT NULL,
            owner_name VARCHAR(100),
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(100),
            opening_time TIME,
            closing_time TIME,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ngo (
            ngo_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            ngo_name VARCHAR(255) NOT NULL,
            capacity INT,
            location TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS food (
            food_id INT AUTO_INCREMENT PRIMARY KEY,
            restaurant_id INT,
            food_name VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            food_type ENUM('Veg', 'Non-Veg') NOT NULL,
            cooked_at DATETIME NOT NULL,
            expiry_time DATETIME NOT NULL,
            status ENUM('Available', 'Claimed') DEFAULT 'Available',
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS deliveries (
            delivery_id INT AUTO_INCREMENT PRIMARY KEY,
            food_id INT,
            ngo_id INT,
            partner_id INT NULL,
            pickup_address TEXT,
            drop_address TEXT,
            status ENUM('Pending', 'Assigned', 'Picked Up', 'Delivered') DEFAULT 'Pending',
            assigned_at DATETIME,
            FOREIGN KEY (food_id) REFERENCES food(food_id) ON DELETE CASCADE,
            FOREIGN KEY (ngo_id) REFERENCES ngo(ngo_id) ON DELETE CASCADE,
            FOREIGN KEY (partner_id) REFERENCES users(user_id) ON DELETE SET NULL
        )
        """
    ]

    for q in queries:
        cursor.execute(q)

    db.commit()
    print("Cloud Database tables created successfully!")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals():
        db.close()
