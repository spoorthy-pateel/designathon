from flask import Blueprint, jsonify, request
from database import SessionLocal
from services.opportunity_service import OpportunityService

opportunity_bp = Blueprint('opportunity', __name__)

def get_service():
    db_session = SessionLocal()
    return OpportunityService(db_session), db_session

@opportunity_bp.route('/getOpportunities', methods=['POST'])
def get_opportunities():
    ids = request.json.get('ids', [])
    service, db = get_service()
    try:
        opportunities = service.get_opportunities_by_ids(ids)
        return jsonify({
            "opportunities": [
                {
                    "id": o.id,
                    "name": o.name,
                    "skills_expected": o.skills_expected,
                    "years_of_experience_required": o.years_of_experience_required,
                    "deadline": o.deadline.isoformat() if o.deadline else None,
                }
                for o in opportunities
            ]
        })
    finally:
        db.close()

@opportunity_bp.route('/getAllOpportunities', methods=['GET'])
def get_all_opportunities():
    service, db = get_service()
    try:
        opportunities = service.get_all_opportunities()
        return jsonify({
            "opportunities": [
                {
                    "id": o.id,
                    "name": o.name,
                    "skills_expected": o.skills_expected,
                    "years_of_experience_required": o.years_of_experience_required,
                    "deadline": o.deadline.isoformat() if o.deadline else None,
                }
                for o in opportunities
            ]
        })
    finally:
        db.close()