from flask import Blueprint, jsonify
from database import mysql
from models.admin import get_all_users, delete_user, get_analytics

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/users", methods=["GET"])
def get_users():
    try:
        users = get_all_users(mysql)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/admin/user/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    try:
        deleted = delete_user(mysql, user_id)
        if deleted:
            return jsonify({"message": "User Deleted Successfully!"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/admin/analytics", methods=["GET"])
def admin_analytics():
    try:
        analytics = get_analytics(mysql)
        return jsonify(analytics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
