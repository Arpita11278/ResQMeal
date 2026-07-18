import MySQLdb
db=MySQLdb.connect(host="b2nefrhzgt6s5ik2rufs-mysql.services.clever-cloud.com", user="u90mrcwewzpcp7wq", passwd="0oHIIMEfeUMH0w8V6jOg", db="b2nefrhzgt6s5ik2rufs")
cursor=db.cursor()
try:
    cursor.execute("INSERT INTO deliveries (food_id, ngo_id, pickup_address, drop_address, status) SELECT 1, 1, r.address, n.location, 'Pending' FROM food f JOIN restaurants r ON f.restaurant_id = r.restaurant_id JOIN ngo n ON n.ngo_id = 1 WHERE f.food_id = 1")
    print("Success")
except Exception as e:
    print(f"Error: {e}")
