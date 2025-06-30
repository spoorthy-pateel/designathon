from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
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
        # Extract data from the request
        data = request.get_json()

        # Validate input
        if not all(key in data for key in ['name', 'skills_expected', 'years_of_experience_required', 'deadline']):
            return jsonify({"error": "Missing required fields"}), 400

        # Call the service method to create the opportunity
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
        return jsonify({"error": str(e)}), 500

    
@opportunity_bp.route('/getOpportunityById/<int:id>', methods=['GET'])
def get_opportunity_by_id(id):
    try:
        # Call the service method to fetch the opportunity by ID
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
        return jsonify({"error": str(e)}), 500


@opportunity_bp.route('/updateOpportunity/<int:id>', methods=['PUT'])
def update_opportunity(id):
    try:
        # Extract data from the request
        data = request.get_json()

        # Call the service method to update the opportunity
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
        return jsonify({"error": str(e)}), 500

@opportunity_bp.route('/deleteOpportunity/<int:id>', methods=['DELETE'])
def delete_opportunity(id):
    try:
        # Call the service method to delete the opportunity by ID
        opportunity_service = get_opportunity_service()
        is_deleted = opportunity_service.delete_opportunity_by_id(id)

        if not is_deleted:
            return jsonify({"error": "Opportunity not found"}), 404

        return jsonify({"message": "Opportunity deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@opportunity_bp.route('/getAllOpportunities', methods=['GET'])
def get_all_opportunities():
    try:
        # Call the service method to fetch all opportunities
        opportunity_service = get_opportunity_service()
        opportunities = opportunity_service.get_all_opportunities()

        if not opportunities:
            return jsonify({"message": "No opportunities found"}), 404

        # Format the response
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
        return jsonify({"error": str(e)}), 500





