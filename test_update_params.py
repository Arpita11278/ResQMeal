import MySQLdb
db=MySQLdb.connect(host="b2nefrhzgt6s5ik2rufs-mysql.services.clever-cloud.com", user="u90mrcwewzpcp7wq", passwd="0oHIIMEfeUMH0w8V6jOg", db="b2nefrhzgt6s5ik2rufs")
cursor=db.cursor()
try:
    cursor.execute("UPDATE food SET status='Claimed' WHERE food_id=%s", (1,))
    db.commit()
    print("Success UPDATE")
except Exception as e:
    print(f"Error: {e}")
