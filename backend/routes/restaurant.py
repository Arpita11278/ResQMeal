from flask import Blueprint, request, jsonify
from database import mysql
from models.restaurant import (
    create_restaurant_profile, 
    get_restaurant_by_id, 
    update_restaurant_profile, 
    get_all_restaurants,
    get_restaurant_by_user
)

restaurant_bp = Blueprint("restaurant", __name__)

@restaurant_bp.route("/restaurant/profile", methods=["POST"])
def create_profile():
    data = request.get_json()
    required_fields = ["user_id", "restaurant_name", "owner_name", "phone", "address", "city", "opening_time", "closing_time"]
    
    # Check if any required field is missing
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
            
    success, err_msg = create_restaurant_profile(mysql, data)
    if not success:
        return jsonify({"error": err_msg}), 400
        
    return jsonify({"message": "Restaurant Profile Created Successfully"}), 201

@restaurant_bp.route("/restaurant/profile/<int:id>", methods=["GET"])
def get_profile(id):
    restaurant = get_restaurant_by_id(mysql, id)
    if restaurant:
        return jsonify(restaurant), 200
    return jsonify({"error": "Restaurant not found"}), 404

@restaurant_bp.route("/restaurant/profile/<int:id>", methods=["PUT"])
def update_profile(id):
    data = request.get_json()
    required_fields = ["restaurant_name", "owner_name", "phone", "address", "city", "opening_time", "closing_time"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
            
    updated = update_restaurant_profile(mysql, id, data)
    if updated:
        return jsonify({"message": "Restaurant Profile Updated Successfully"}), 200
    return jsonify({"error": "Restaurant not found"}), 404

@restaurant_bp.route("/restaurants", methods=["GET"])
def get_all():
    restaurants = get_all_restaurants(mysql)
    return jsonify(restaurants), 200
