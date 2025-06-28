from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from models.consultant import Consultant
from services.consultant_service import ConsultantService

consultant_bp = Blueprint('consultant', __name__)

# Dependency injection for the service layer
def get_consultant_service():
    db_session: Session = SessionLocal()
    return ConsultantService(db_session)

@consultant_bp.route('/addConsultant', methods=['POST'])
def add_consultant():
    try:
        data = request.json
        name = data.get('name')
        emp_id = data.get('emp_id')
        mobile_no = data.get('mobile_no')
        email = data.get('email')
        address = data.get('address')
        current_role = data.get('current_role')
        user_id = data.get('user_id')  # <-- Accept user_id from frontend

        # Validate required fields
        if not name or not emp_id or not mobile_no or not email or not user_id:
            return jsonify({"error": "Missing required fields"}), 400

        consultant_service = get_consultant_service()

        # Pass user_id to the service
        new_consultant, error = consultant_service.add_consultant(
            name=name,
            emp_id=emp_id,
            mobile_no=mobile_no,
            email=email,
            address=address,
            current_role=current_role,
            user_id=user_id  # <-- Pass user_id to service
        )

        if error:
            return jsonify({"error": error}), 400

        return jsonify({
            "message": "Consultant added successfully",
            "consultant": {
                "id": new_consultant.id,
                "name": new_consultant.name,
                "emp_id": new_consultant.emp_id,
                "mobile_no": new_consultant.mobile_no,
                "email": new_consultant.email,
                "address": new_consultant.address,
                "current_role": new_consultant.current_role
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@consultant_bp.route('/getConsultantById/<int:consultant_id>', methods=['GET'])
def get_consultant(consultant_id):
    try:
        consultant_service = get_consultant_service()
        consultant, error = consultant_service.get_consultant(consultant_id)
        if error:
            return jsonify({"error": error}), 404

        return jsonify({
            "consultant": {
                "id": consultant.id,
                "name": consultant.name,
                "emp_id": consultant.emp_id,
                "mobile_no": consultant.mobile_no,
                "email": consultant.email,
                "address": consultant.address,
                "current_role": consultant.current_role
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@consultant_bp.route('/getAllConsultants', methods=['GET'])
def get_all_consultants():
    try:
        consultant_service = get_consultant_service()
        consultants = consultant_service.get_all_consultants()

        return jsonify({
            "consultants": [
                {
                    "id": consultant.id,
                    "name": consultant.name,
                    "emp_id": consultant.emp_id,
                    "mobile_no": consultant.mobile_no,
                    "email": consultant.email,
                    "address": consultant.address,
                    "current_role": consultant.current_role
                }
                for consultant in consultants
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@consultant_bp.route('/updateConsultant/<int:consultant_id>',methods=['PUT'])
def update_consultant(consultant_id):
    try:
        data = request.json

        data.pop('user_id', None)

        consultant_service = get_consultant_service()
        consultant, error = consultant_service.update_consultant(consultant_id, **data)
        if error:
            return jsonify({"error": error}), 404

        return jsonify({
            "message": "Consultant updated successfully",
            "consultant": {
                "id": consultant.id,
                "name": consultant.name,
                "emp_id": consultant.emp_id,
                "mobile_no": consultant.mobile_no,
                "email": consultant.email,
                "address": consultant.address,
                "current_role": consultant.current_role
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@consultant_bp.route('/deleteConsultant/<int:consultant_id>',methods=['DELETE'])
def delete_consultant(consultant_id):
    try:
        consultant_service = get_consultant_service()
        success, error = consultant_service.delete_consultant(consultant_id)
        if error:
            return jsonify({"error": error}), 404

        return jsonify({"message": "Consultant deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@consultant_bp.route('/getConsultantByEmpId/<emp_id>', methods=['GET'])
def get_consultant_by_emp_id(emp_id):
    try:
        consultant_service = get_consultant_service()
        consultant = consultant_service.get_consultant_by_emp_id(emp_id)
        if not consultant:
            return jsonify({"error": f"No consultant found with emp_id {emp_id}"}), 404
        return jsonify({
            "consultant": {
                "id": consultant.id,
                "name": consultant.name,
                "emp_id": consultant.emp_id,
                "mobile_no": consultant.mobile_no,
                "email": consultant.email,
                "address": consultant.address,
                "current_role": consultant.current_role
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
