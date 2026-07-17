from flask import Blueprint, request, jsonify
from models.user import create_user, verify_user
from database import mysql  # Import the real mysql object

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    required = ["name", "email", "password", "role"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    result = create_user(
        mysql,
        data["name"],
        data["email"],
        data["password"],
        data["role"]
    )

    return jsonify(result)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Requirement 9: Handle missing fields (Status 400)
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Missing email or password"}), 400

    email = data["email"]
    password = data["password"]

    # Requirements 5 & 6: Verify email and password in the database
    is_valid = verify_user(mysql, email, password)

    # Requirement 7: Successful login (Status 200)
    if is_valid:
        return jsonify({"message": "Login Successful"}), 200
        
    # Requirement 8: Invalid login (Status 401)
    else:
        return jsonify({"message": "Invalid Email or Password"}), 401