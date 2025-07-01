from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from models.training import TrainingLevel
from services.training_service import TrainingService

# Create a Blueprint for training-related routes
training_bp = Blueprint('training', __name__)

# Dependency injection for the service layer
def get_training_service():
    db_session: Session = SessionLocal()
    return TrainingService(db_session)

@training_bp.route('/addTraining', methods=['POST'])
def add_training():
    try:
        data = request.json
        training_name = data.get('training_name')
        technologies_learnt = data.get('technologies_learnt')
        level_of_training = data.get('level_of_training')
        duration = data.get('duration')

        # Validate required fields
        if not training_name or not technologies_learnt or not level_of_training or not duration:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate level_of_training
        try:
            level_enum = TrainingLevel(level_of_training)
        except ValueError:
            return jsonify({"error": f"Invalid level_of_training. Allowed values: {', '.join([level.value for level in TrainingLevel])}"}), 400

        # Call the service method to add the training
        training_service = get_training_service()
        new_training = training_service.add_training(training_name, technologies_learnt, level_enum, duration)

        return jsonify({
            "message": "Training added successfully",
            "training": {
                "id": new_training.id,
                "training_name": new_training.training_name,
                "technologies_learnt": new_training.technologies_learnt,
                "level_of_training": new_training.level_of_training.value,
                "duration": new_training.duration
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@training_bp.route('/updateTraining/<int:training_id>', methods=['PUT'])
def update_training(training_id):
    try:
        data = request.json
        training_name = data.get('training_name')
        technologies_learnt = data.get('technologies_learnt')
        level_of_training = data.get('level_of_training')
        duration = data.get('duration')

        # Validate required fields
        if not training_name and not technologies_learnt and not level_of_training and not duration:
            return jsonify({"error": "No fields provided for update"}), 400

        # Validate level_of_training if provided
        level_enum = None
        if level_of_training:
            try:
                level_enum = TrainingLevel(level_of_training)
            except ValueError:
                return jsonify({"error": f"Invalid level_of_training. Allowed values: {', '.join([level.value for level in TrainingLevel])}"}), 400

        # Call the service method to update the training
        training_service = get_training_service()
        updated_training = training_service.update_training(training_id, training_name, technologies_learnt, level_enum, duration)

        if updated_training:
            return jsonify({
                "message": "Training updated successfully",
                "training": {
                    "id": updated_training.id,
                    "training_name": updated_training.training_name,
                    "technologies_learnt": updated_training.technologies_learnt,
                    "level_of_training": updated_training.level_of_training.value,
                    "duration": updated_training.duration
                }
            }), 200
        else:
            return jsonify({"error": "Training not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@training_bp.route('/getTraining/<int:training_id>', methods=['GET'])
def get_training(training_id):
    try:
        # Call the service method to fetch the training
        training_service = get_training_service()
        training = training_service.get_training_by_id(training_id)

        if training:
            return jsonify({
                "id": training.id,
                "training_name": training.training_name,
                "technologies_learnt": training.technologies_learnt,
                "level_of_training": training.level_of_training.value,
                "duration": training.duration
            }), 200
        else:
            return jsonify({"error": "Training not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@training_bp.route('/getAllTrainings', methods=['GET'])
def get_all_trainings():
    try:
        # Call the service method
        training_service = get_training_service()
        trainings = training_service.get_all_trainings()

        # Format the response
        # training_list = [
        #     {
        #         "id": training.id,
        #         "training_name": training.training_name,
        #         "technologies_learnt": training.technologies_learnt,
        #         "level_of_training": training.level_of_training.value,
        #         "duration": training.duration
        #     }
        #     for training in trainings
        # ]

        return jsonify({
            "message": "Trainings retrieved successfully",
            "trainings": [
            {
                "id": training.id,
                "training_name": training.training_name,
                "technologies_learnt": training.technologies_learnt,
                "level_of_training": training.level_of_training.value,
                "duration": training.duration
            }
            for training in trainings
        ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@training_bp.route('/deleteTraining/<int:training_id>', methods=['DELETE'])
def delete_training(training_id):
    try:
        # Call the service method to delete the training
        training_service = get_training_service()
        deleted_training = training_service.delete_training_by_id(training_id)
        print(vars(deleted_training))

        if deleted_training:
            return jsonify({
                "message": "Training deleted successfully",
                "training": {
                    "id": deleted_training.id,
                    "training_name": deleted_training.training_name,
                    # "technologies_learnt": deleted_training.technologies_learnt,
                    #  "level_of_training": deleted_training.level_of_training.value,
                    #  "duration": deleted_training.duration
                }
            }), 200
        else:
            return jsonify({"error": "Training not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@training_bp.route('/getTrainingsByIds', methods=['POST'])
def get_trainings_by_ids():
    try:
        data = request.json
        ids = data.get('ids', [])
        if not isinstance(ids, list) or not ids:
            return jsonify({"error": "List of training IDs required"}), 400

        training_service = get_training_service()
        trainings = training_service.get_trainings_by_ids(ids)

        return jsonify([
            {
                "id": training.id,
                "training_name": training.training_name,
                "technologies_learnt": training.technologies_learnt,
                "level_of_training": training.level_of_training.value,
                "duration": training.duration
            }
            for training in trainings
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500