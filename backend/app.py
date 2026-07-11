from flask import Flask
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB

mysql = MySQL(app)

@app.route("/")
def home():
    return "ResQMeal API Running Successfully"

@app.route("/users")
def users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    return str(data)

if __name__ == "__main__":
    app.run(debug=True)