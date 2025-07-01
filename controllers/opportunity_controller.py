from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
import traceback  # <-- Add this import

from database import SessionLocal
from services.opportunity_service import OpportunityService

opportunity_bp = Blueprint('opportunity', __name__)

# Dependency injection for the service layer
def get_opportunity_service():
    db_session: Session = SessionLocal()
    return OpportunityService(db_session)

@opportunity_bp.route('/createOpportunity', methods=['POST'])
def create_opportunity():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'skills_expected', 'years_of_experience_required', 'deadline']):
            return jsonify({"error": "Missing required fields"}), 400

        opportunity_service = get_opportunity_service()
        new_opportunity = opportunity_service.create_opportunity(
            name=data['name'],
            skills_expected=data['skills_expected'],
            years_of_experience_required=data['years_of_experience_required'],
            deadline=data['deadline']
        )

        return jsonify({
            "message": "Opportunity created successfully",
            "opportunity": {
                "id": new_opportunity.id,
                "name": new_opportunity.name,
                "skills_expected": new_opportunity.skills_expected,
                "years_of_experience_required": new_opportunity.years_of_experience_required,
                "deadline": new_opportunity.deadline.isoformat()
            }
        }), 201
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@opportunity_bp.route('/getOpportunityById/<int:id>', methods=['GET'])
def get_opportunity_by_id(id):
    try:
        opportunity_service = get_opportunity_service()
        opportunity = opportunity_service.get_opportunity_by_id(id)

        if not opportunity:
            return jsonify({"error": "Opportunity not found"}), 404

        return jsonify({
            "message": "Opportunity retrieved successfully",
            "opportunity": {
                "id": opportunity.id,
                "name": opportunity.name,
                "skills_expected": opportunity.skills_expected,
                "years_of_experience_required": opportunity.years_of_experience_required,
                "deadline": opportunity.deadline.isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@opportunity_bp.route('/updateOpportunity/<int:id>', methods=['PUT'])
def update_opportunity(id):
    try:
        data = request.get_json()
        opportunity_service = get_opportunity_service()
        updated_opportunity = opportunity_service.update_opportunity(
            id=id,
            name=data.get('name'),
            skills_expected=data.get('skills_expected'),
            years_of_experience_required=data.get('years_of_experience_required'),
            deadline=data.get('deadline')
        )

        if not updated_opportunity:
            return jsonify({"error": "Opportunity not found"}), 404

        return jsonify({
            "message": "Opportunity updated successfully",
            "opportunity": {
                "id": updated_opportunity.id,
                "name": updated_opportunity.name,
                "skills_expected": updated_opportunity.skills_expected,
                "years_of_experience_required": updated_opportunity.years_of_experience_required,
                "deadline": updated_opportunity.deadline.isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@opportunity_bp.route('/deleteOpportunity/<int:id>', methods=['DELETE'])
def delete_opportunity(id):
    try:
        opportunity_service = get_opportunity_service()
        is_deleted = opportunity_service.delete_opportunity_by_id(id)

        if not is_deleted:
            return jsonify({"error": "Opportunity not found"}), 404

        return jsonify({"message": "Opportunity deleted successfully"}), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@opportunity_bp.route('/getAllOpportunities', methods=['GET'])
def get_all_opportunities():
    try:
        opportunity_service = get_opportunity_service()
        opportunities = opportunity_service.get_all_opportunities()

        if not opportunities:
            return jsonify({"message": "No opportunities found"}), 404

        opportunity_list = [
            {
                "id": opportunity.id,
                "name": opportunity.name,
                "skills_expected": opportunity.skills_expected,
                "years_of_experience_required": opportunity.years_of_experience_required,
                "deadline": opportunity.deadline.isoformat()
            }
            for opportunity in opportunities
        ]

        return jsonify({
            "message": "Opportunities retrieved successfully",
            "opportunities": opportunity_list
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@opportunity_bp.route('/getOpportunities', methods=['POST', 'OPTIONS'])
def get_opportunities():
    if request.method == 'OPTIONS':
        return '', 200  # Handles CORS preflight

    try:
        data = request.get_json() or {}
        ids = data.get('ids', [])
        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            return jsonify({"error": "Invalid or missing 'ids'. It should be a list of integers."}), 400

        opportunity_service = get_opportunity_service()
        opportunities = opportunity_service.get_opportunities_by_ids(ids)

        opportunity_list = [
            {
                "id": o.id,
                "name": o.name,
                "skills_expected": o.skills_expected,
                "years_of_experience_required": o.years_of_experience_required,
                "deadline": o.deadline.isoformat() if o.deadline else None,
            }
            for o in opportunities
        ]
        return jsonify({
            "opportunities": opportunity_list
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500