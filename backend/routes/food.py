from flask import Blueprint, request, jsonify
from database import mysql
from models.food import donate_food, get_available_food, update_food_status, delete_food, get_food_by_restaurant

food_bp = Blueprint("food", __name__)

@food_bp.route("/food/donate", methods=["POST"])
def donate_food():
    data = request.get_json()
    
    required_fields = ["restaurant_id", "food_name", "quantity", "food_type", "cooked_at", "expiry_time"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
            
    try:
        donate_food(mysql, data)
        return jsonify({"message": "Food Donation Added Successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route("/food/available", methods=["GET"])
def available_food():
    try:
        foods = get_available_food(mysql)
        return jsonify(foods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route("/food/update/<int:id>", methods=["PUT"])
def update_food(id):
    data = request.get_json()
    if "status" not in data:
        return jsonify({"error": "status is required"}), 400
        
    try:
        updated = update_food_status(mysql, id, data["status"])
        if updated:
            return jsonify({"message": "Food status updated successfully"}), 200
        else:
            return jsonify({"error": "Food item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route("/food/delete/<int:id>", methods=["DELETE"])
def remove_food(id):
    try:
        deleted = delete_food(mysql, id)
        if deleted:
            return jsonify({"message": "Food deleted successfully"}), 200
        else:
            return jsonify({"error": "Food item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route("/food/restaurant/<int:restaurant_id>", methods=["GET"])
def get_restaurant_food(restaurant_id):
    try:
        foods = get_food_by_restaurant(mysql, restaurant_id)
        return jsonify(foods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
