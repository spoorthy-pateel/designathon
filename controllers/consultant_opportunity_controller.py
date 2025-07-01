from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from models.consultant_opportunity import SelectionStatus 
from services.consultant_opportunity_service import ConsultantOpportunityService
import traceback

# Create a Blueprint for consultant opportunity-related routes
consultant_opportunity_bp = Blueprint('consultantOpportunity', __name__)

# Dependency injection for the service layer
def get_consultant_opportunity_service():
    db_session: Session = SessionLocal()
    return ConsultantOpportunityService(db_session), db_session

@consultant_opportunity_bp.route('/addConsultantOpportunity', methods=['POST'])
def add_consultant_opportunity():
    db_session = None
    try:
        data = request.json
        consultant_id = data.get('consultant_id')
        opportunity_id = data.get('opportunity_id')
        selection_status = data.get('selection_status')
        remarks = data.get('remarks')

        if not consultant_id or not opportunity_id or not selection_status:
            return jsonify({"error": "Missing required fields"}), 400

        valid_statuses = ["Selected", "Rejected", "Pending"]
        if selection_status not in valid_statuses:
            return jsonify({"error": f"Invalid selection status. Must be one of {valid_statuses}"}), 400

        consultant_opportunity_service, db_session = get_consultant_opportunity_service()
        new_consultant_opportunity = consultant_opportunity_service.add_consultant_opportunity(
            consultant_id, opportunity_id, selection_status, remarks
        )

        return jsonify({
            "message": "Consultant opportunity added successfully",
            "consultant_opportunity": {
                "id": new_consultant_opportunity.id,
                "consultant_id": new_consultant_opportunity.consultant_id,
                "opportunity_id": new_consultant_opportunity.opportunity_id,
                "selection_status": new_consultant_opportunity.selection_status.value,
                "remarks": new_consultant_opportunity.remarks
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
    finally:
        if db_session:
            db_session.close()

@consultant_opportunity_bp.route('/getConsultantOpportunityById/<int:id>', methods=['GET'])
def get_consultant_opportunity_by_id(id):
    db_session = None
    try:
        consultant_opportunity_service, db_session = get_consultant_opportunity_service()
        consultant_opportunity = consultant_opportunity_service.get_consultant_opportunity_by_id(id)

        if not consultant_opportunity:
            return jsonify({"error": "Consultant opportunity not found"}), 404

        return jsonify({
            "message": "Consultant opportunity retrieved successfully",
            "consultant_opportunity": {
                "id": consultant_opportunity.id,
                "consultant_id": consultant_opportunity.consultant_id,
                "opportunity_id": consultant_opportunity.opportunity_id,
                "selection_status": consultant_opportunity.selection_status.value,
                "remarks": consultant_opportunity.remarks
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
    finally:
        if db_session:
            db_session.close()

@consultant_opportunity_bp.route('/updateConsultantOpportunity/<int:id>', methods=['PUT'])
def update_consultant_opportunity(id):
    db_session = None
    try:
        data = request.get_json()
        consultant_opportunity_service, db_session = get_consultant_opportunity_service()
        updated_consultant_opportunity = consultant_opportunity_service.update_consultant_opportunity(
            id=id,
            consultant_id=data.get('consultant_id'),
            opportunity_id=data.get('opportunity_id'),
            selection_status=data.get('selection_status'),
            remarks=data.get('remarks')
        )

        if not updated_consultant_opportunity:
            return jsonify({"error": "Consultant opportunity not found"}), 404

        return jsonify({
            "message": "Consultant opportunity updated successfully",
            "consultant_opportunity": {
                "id": updated_consultant_opportunity.id,
                "consultant_id": updated_consultant_opportunity.consultant_id,
                "opportunity_id": updated_consultant_opportunity.opportunity_id,
                "selection_status": updated_consultant_opportunity.selection_status.value,
                "remarks": updated_consultant_opportunity.remarks
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
    finally:
        if db_session:
            db_session.close()

@consultant_opportunity_bp.route('/deleteConsultantOpportunity/<int:id>', methods=['DELETE'])
def delete_consultant_opportunity(id):
    db_session = None
    try:
        consultant_opportunity_service, db_session = get_consultant_opportunity_service()
        is_deleted = consultant_opportunity_service.delete_consultant_opportunity_by_id(id)

        if not is_deleted:
            return jsonify({"error": "Consultant opportunity not found"}), 404

        return jsonify({"message": "Consultant opportunity deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
    finally:
        if db_session:
            db_session.close()

@consultant_opportunity_bp.route('/getAllConsultantOpportunities', methods=['GET'])
def get_all_consultant_opportunities():
    db_session = None
    try:
        consultant_opportunity_service, db_session = get_consultant_opportunity_service()
        consultant_opportunities = consultant_opportunity_service.get_all_consultant_opportunities()

        if not consultant_opportunities:
            return jsonify({"message": "No consultant opportunities found"}), 404

        consultant_opportunity_list = [
            {
                "id": co.id,
                "consultant_id": co.consultant_id,
                "opportunity_id": co.opportunity_id,
                "selection_status": co.selection_status.value,
                "remarks": co.remarks
            }
            for co in consultant_opportunities
        ]

        return jsonify({
            "message": "Consultant opportunities retrieved successfully",
            "consultant_opportunities": consultant_opportunity_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
    finally:
        if db_session:
            db_session.close()
            
@consultant_opportunity_bp.route('/getOpportunitiesByConsultant/<int:consultant_id>', methods=['GET'])
def get_opportunities_by_consultant(consultant_id):
    db_session = None
    try:
        consultant_opportunity_service, db_session = get_consultant_opportunity_service()
        consultant_opportunities = consultant_opportunity_service.get_consultant_opportunity_by_consultant_id(consultant_id)

        if not consultant_opportunities:
            return jsonify({"message": "No consultant opportunities found"}), 404

        consultant_opportunity_list = [
            {
                "id": co.id,
                "consultant_id": co.consultant_id,
                "opportunity_id": co.opportunity_id,
                "selection_status": co.selection_status.value,
                "remarks": co.remarks
            }
            for co in consultant_opportunities
        ]

        return jsonify({
            "message": "Consultant opportunities retrieved successfully",
            "opportunities": consultant_opportunity_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
    finally:
        if db_session:
            db_session.close()
