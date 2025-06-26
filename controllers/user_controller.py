from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import Role
from services.user_service import UserService

# Create a Blueprint for user-related routes
user_bp = Blueprint('user', __name__)

# Dependency injection for the service layer
def get_user_service():
    db_session: Session = SessionLocal()
    return UserService(db_session)

@user_bp.route('/addUser', methods=['POST'])
def add_user():
    try:
        data = request.json
        emp_id = data.get('emp_id')
        password = data.get('password')
        role = data.get('role')

        if not emp_id or not password or not role:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            role_enum = Role(role)
        except ValueError:
            return jsonify({"error": f"Invalid role. Allowed values: {', '.join([r.value for r in Role])}"}), 400

        user_service = get_user_service()
        new_user = user_service.add_user(emp_id, password, role_enum)

        return jsonify({
            "message": "User added successfully",
            "user": {
                "id": new_user.user_id,
                "emp_id": new_user.emp_id,
                "role": new_user.role.value
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        # Parse JSON data from the request
        data = request.json
        emp_id = data.get('emp_id')
        password = data.get('password')

        # Validate input
        if not emp_id or not password:
            return jsonify({"error": "Missing employee id or password"}), 400

        # Get the user service
        user_service = get_user_service()

        # Validate the user
        user, error = user_service.validate_user(emp_id, password)

        if error:
            return jsonify({"error": error}), 401

        # Return success response
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.user_id,
                "emp_id": user.emp_id,
                "role": user.role.value
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500