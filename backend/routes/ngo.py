from flask import Blueprint, request, jsonify
from database import mysql
from models.ngo import accept_food_donation, get_ngo_history, create_ngo_profile

ngo_bp = Blueprint("ngo", __name__)

@ngo_bp.route("/ngo/accept", methods=["POST"])
def accept_food():
    data = request.get_json()
    if "food_id" not in data or "ngo_id" not in data:
        return jsonify({"error": "food_id and ngo_id are required"}), 400
        
    try:
        accept_food_donation(mysql, data["food_id"], data["ngo_id"])
        return jsonify({"message": "Food Accepted Successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ngo_bp.route("/ngo/history/<int:ngo_id>", methods=["GET"])
def ngo_history(ngo_id):
    try:
        history = get_ngo_history(mysql, ngo_id)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ngo_bp.route("/ngo/profile", methods=["POST"])
def add_ngo_profile():
    data = request.get_json()
    if "user_id" not in data or "ngo_name" not in data:
        return jsonify({"error": "user_id and ngo_name are required"}), 400
        
    success, err_msg = create_ngo_profile(mysql, data)
    if not success:
        return jsonify({"error": err_msg}), 400
        
    return jsonify({"message": "NGO Profile Created Successfully"}), 201
