from flask import Blueprint, request, jsonify
from services.consultant_opportunity_service import (
    create_consultant_opportunity,
    get_consultant_opportunities_by_consultant,
    update_selection_status,
    get_by_id
)
from models.consultant_opportunity import SelectionStatus

consultant_opportunity_bp = Blueprint('consultant_opportunity', __name__)

@consultant_opportunity_bp.route('/create', methods=['POST'])
def create():
    data = request.json
    consultant_id = data.get('consultant_id')
    opportunity_id = data.get('opportunity_id')
    remarks = data.get('remarks')
    selection_status = data.get('selection_status', 'pending')
    status_enum = SelectionStatus[selection_status] if isinstance(selection_status, str) else selection_status

    co = create_consultant_opportunity(consultant_id, opportunity_id, status_enum, remarks)
    return jsonify({
        "id": co.id,
        "consultant_id": co.consultant_id,
        "opportunity_id": co.opportunity_id,
        "selection_status": co.selection_status.value,
        "remarks": co.remarks
    })

@consultant_opportunity_bp.route('/by-consultant/<int:consultant_id>', methods=['GET'])
def get_by_consultant(consultant_id):
    results = get_consultant_opportunities_by_consultant(consultant_id)
    return jsonify([
        {
            "id": co.id,
            "consultant_id": co.consultant_id,
            "opportunity_id": co.opportunity_id,
            "selection_status": co.selection_status.value,
            "remarks": co.remarks
        } for co in results
    ])

@consultant_opportunity_bp.route('/update-status/<int:co_id>', methods=['PATCH'])
def update_status(co_id):
    data = request.json
    status = data.get('selection_status')
    remarks = data.get('remarks')
    status_enum = SelectionStatus[status] if isinstance(status, str) else status
    co = update_selection_status(co_id, status_enum, remarks)
    if not co:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": co.id,
        "consultant_id": co.consultant_id,
        "opportunity_id": co.opportunity_id,
        "selection_status": co.selection_status.value,
        "remarks": co.remarks
    })

@consultant_opportunity_bp.route('/<int:co_id>', methods=['GET'])
def get_one(co_id):
    co = get_by_id(co_id)
    if not co:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": co.id,
        "consultant_id": co.consultant_id,
        "opportunity_id": co.opportunity_id,
        "selection_status": co.selection_status.value,
        "remarks": co.remarks
    })