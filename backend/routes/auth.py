from flask import Blueprint, request, jsonify
from models.user import create_user
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