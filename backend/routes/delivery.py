from flask import Blueprint, request, jsonify
from database import mysql
from models.delivery import assign_delivery, update_delivery_status, get_delivery_tasks

delivery_bp = Blueprint("delivery", __name__)

@delivery_bp.route("/delivery/assign", methods=["POST"])
def assign():
    data = request.get_json()
    if "delivery_id" not in data or "partner_id" not in data:
        return jsonify({"error": "delivery_id and partner_id are required"}), 400
        
    try:
        assign_delivery(mysql, data)
        return jsonify({"message": "Delivery Assigned Successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_bp.route("/delivery/available", methods=["GET"])
def available_deliveries():
    try:
        from models.delivery import get_available_deliveries
        tasks_list = get_available_deliveries(mysql)
        return jsonify(tasks_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_bp.route("/delivery/update/<int:delivery_id>", methods=["PUT"])
def update_status(delivery_id):
    data = request.get_json()
    if "status" not in data or "time" not in data:
        return jsonify({"error": "status and time are required in JSON body"}), 400
        
    status = data["status"]
    time_value = data["time"]
    
    if status == "Picked Up":
        time_field = "pickup_time"
    elif status == "Delivered":
        time_field = "delivery_time"
    else:
        return jsonify({"error": "Invalid status. Must be 'Picked Up' or 'Delivered'"}), 400
        
    try:
        updated = update_delivery_status(mysql, delivery_id, status, time_field, time_value)
        if updated:
            return jsonify({"message": f"Status successfully updated to {status}"}), 200
        return jsonify({"error": "Delivery task not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delivery_bp.route("/delivery/tasks/<int:partner_id>", methods=["GET"])
def tasks(partner_id):
    try:
        tasks_list = get_delivery_tasks(mysql, partner_id)
        return jsonify(tasks_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
