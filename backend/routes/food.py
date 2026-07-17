from flask import Blueprint, request, jsonify
from database import mysql
from models.food import donate_food, get_available_food, update_food, delete_food

food_bp = Blueprint("food", __name__)

@food_bp.route("/food/donate", methods=["POST"])
def add_food():
    data = request.get_json()
    required_fields = ["restaurant_id", "food_name", "quantity", "food_type", "cooked_at", "expiry_time"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
            
    try:
        donate_food(mysql, data)
        return jsonify({"message": "Food Donated Successfully"}), 201
    except Exception as e:
        return jsonify({"error": "Invalid Restaurant ID or Database Error", "details": str(e)}), 400

@food_bp.route("/food/available", methods=["GET"])
def get_food():
    try:
        foods = get_available_food(mysql)
        return jsonify(foods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route("/food/update/<int:id>", methods=["PUT"])
def edit_food(id):
    data = request.get_json()
    required_fields = ["food_name", "quantity", "food_type", "cooked_at", "expiry_time"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
            
    try:
        updated = update_food(mysql, id, data)
        if updated:
            return jsonify({"message": "Food Details Updated Successfully"}), 200
        return jsonify({"error": "Food item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route("/food/delete/<int:id>", methods=["DELETE"])
def remove_food(id):
    try:
        deleted = delete_food(mysql, id)
        if deleted:
            return jsonify({"message": "Food Item Deleted Successfully"}), 200
        return jsonify({"error": "Food item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
