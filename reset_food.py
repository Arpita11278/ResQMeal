import MySQLdb
db = MySQLdb.connect(host='b2nefrhzgt6s5ik2rufs-mysql.services.clever-cloud.com', user='u90mrcwewzpcp7wq', passwd='0oHIIMEfeUMH0w8V6jOg', db='b2nefrhzgt6s5ik2rufs')
cursor = db.cursor()
cursor.execute("UPDATE food SET status = 'Available'")
db.commit()
print('Done')
