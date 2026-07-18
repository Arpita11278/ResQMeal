from flask import Flask, request, jsonify
from flask_cors import CORS
import config
from database import mysql
from routes.auth import auth_bp
from routes.restaurant import restaurant_bp
from routes.food import food_bp
from routes.ngo import ngo_bp
from routes.delivery import delivery_bp
from routes.admin import admin_bp

app = Flask(__name__)
CORS(app)

app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB

mysql.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(restaurant_bp) 
app.register_blueprint(food_bp)
app.register_blueprint(ngo_bp)
app.register_blueprint(delivery_bp)
app.register_blueprint(admin_bp)

@app.route("/")
def home():
    return {"status": "ResQMeal API is live and running!"}

@app.route("/users")
def users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    return str(data)

if __name__ == "__main__":
    app.run(debug=True)