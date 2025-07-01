from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from services.consultant_training_service import ConsultantTrainingService
import traceback

consultant_training_bp = Blueprint('consultant_training', __name__)

def get_consultant_training_service(db_session):
    return ConsultantTrainingService(db_session)

@consultant_training_bp.route('/addConsultantTraining', methods=['POST'])
def add_consultant_training():
    db_session: Session = SessionLocal()
    try:
        data = request.json
        consultant_id = data.get('consultant_id')
        training_id = data.get('training_id')
        attended_hours = data.get('attended_hours')
        if not consultant_id or not training_id or attended_hours is None:
            return jsonify({"error": "Missing required fields"}), 400
        if attended_hours < 0:
            return jsonify({"error": "Attended hours cannot be negative"}), 400
        consultant_training_service = get_consultant_training_service(db_session)
        new_consultant_training = consultant_training_service.add_consultant_training(
            consultant_id, training_id, attended_hours
        )
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
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    finally:
        db_session.close()

@consultant_training_bp.route('/updateConsultantTraining/<int:id>', methods=['PUT'])
def update_consultant_training(id):
    db_session: Session = SessionLocal()
    try:
        data = request.json
        consultant_id = data.get('consultant_id')
        training_id = data.get('training_id')
        attended_hours = data.get('attended_hours')
        if consultant_id is None or training_id is None or attended_hours is None:
            return jsonify({"error": "Missing required fields"}), 400
        if attended_hours <= 0:
            return jsonify({"error": "Attended hours must be greater than 0"}), 400
        consultant_training_service = get_consultant_training_service(db_session)
        updated_consultant_training = consultant_training_service.update_consultant_training(
            id, consultant_id, training_id, attended_hours
        )
        if not updated_consultant_training:
            return jsonify({"error": "Consultant training not found"}), 404
        return jsonify({
            "message": "Consultant training updated successfully",
            "consultant_training": {
                "id": updated_consultant_training.id,
                "consultant_id": updated_consultant_training.consultant_id,
                "training_id": updated_consultant_training.training_id,
                "attended_hours": updated_consultant_training.attended_hours
            }
        }), 200
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    finally:
        db_session.close()

@consultant_training_bp.route('/getConsultantTraining/<int:id>', methods=['GET'])
def get_consultant_training_by_id(id):
    db_session: Session = SessionLocal()
    try:
        consultant_training_service = get_consultant_training_service(db_session)
        consultant_training = consultant_training_service.get_consultant_training_by_id(id)
        if not consultant_training:
            return jsonify({"error": "Consultant training not found"}), 404
        return jsonify({
            "message": "Consultant training retrieved successfully",
            "consultant_training": {
                "id": consultant_training.id,
                "consultant_id": consultant_training.consultant_id,
                "training_id": consultant_training.training_id,
                "attended_hours": consultant_training.attended_hours
            }
        }), 200
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    finally:
        db_session.close()

@consultant_training_bp.route('/deleteConsultantTraining/<int:id>', methods=['DELETE'])
def delete_consultant_training_by_id(id):
    db_session: Session = SessionLocal()
    try:
        consultant_training_service = get_consultant_training_service(db_session)
        is_deleted = consultant_training_service.delete_consultant_training_by_id(id)
        if not is_deleted:
            return jsonify({"error": "Consultant training not found"}), 404
        return jsonify({"message": "Consultant training deleted successfully"}), 200
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    finally:
        db_session.close()

@consultant_training_bp.route('/getAllConsultantTrainings', methods=['GET'])
def get_all_consultant_trainings():
    db_session: Session = SessionLocal()
    try:
        consultant_training_service = get_consultant_training_service(db_session)
        consultant_trainings = consultant_training_service.get_all_consultant_trainings()
        consultant_training_list = [
            {
                "id": ct.id,
                "consultant_id": ct.consultant_id,
                "training_id": ct.training_id,
                "attended_hours": ct.attended_hours
            }
            for ct in consultant_trainings
        ]
        return jsonify({
            "message": "Consultant trainings retrieved successfully",
            "consultant_trainings": consultant_training_list
        }), 200
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    finally:
        db_session.close()

@consultant_training_bp.route('/getConsultantTrainingsByConsultantId/<int:consultant_id>', methods=['GET'])
def get_consultant_trainings_by_consultant_id(consultant_id):
    db_session: Session = SessionLocal()
    try:
        consultant_training_service = get_consultant_training_service(db_session)
        consultant_trainings = consultant_training_service.get_consultant_trainings_by_consultant_id(consultant_id)

        consultant_training_list = [
            {
                "id": ct.id,
                "consultant_id": ct.consultant_id,
                "training_id": ct.training_id,
                "attended_hours": ct.attended_hours
            }
            for ct in consultant_trainings
        ]

        return jsonify({
            "message": "Consultant trainings retrieved successfully",
            "consultant_trainings": consultant_training_list
        }), 200
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    finally:
        db_session.close()