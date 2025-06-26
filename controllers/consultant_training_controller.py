from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from services.consultant_training_service import ConsultantTrainingService

# Create a Blueprint for consultant training-related routes
consultant_training_bp = Blueprint('consultant_training', __name__)

# Dependency injection for the service layer
def get_consultant_training_service():
    db_session: Session = SessionLocal()
    return ConsultantTrainingService(db_session)

@consultant_training_bp.route('/addConsultantTraining', methods=['POST'])
def add_consultant_training():
    try:
        data = request.json
        consultant_id = data.get('consultant_id')
        training_id = data.get('training_id')
        attended_hours = data.get('attended_hours')

        # print("The consultant controller is started."+attended_hours)

        # Validate required fields
        if not consultant_id or not training_id or attended_hours is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate attended_hours
        if attended_hours <= 0:
            return jsonify({"error": "Attended hours must be greater than 0"}), 400

        # Call the service method to add the consultant training
        consultant_training_service = get_consultant_training_service()
        new_consultant_training = consultant_training_service.add_consultant_training(
            consultant_id, training_id, attended_hours
        )
        
        # print("The mehod is calling 2 times"+consultant_training.consultant_id)

        return jsonify({
            "message": "Consultant training added successfully",
            "consultant_training": {
                "id": new_consultant_training.id,
                "consultant_id": new_consultant_training.consultant_id,
                "training_id": new_consultant_training.training_id,
                "attended_hours": new_consultant_training.attended_hours
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
