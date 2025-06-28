from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import SessionLocal
from services.skills_service import SkillsService

skills_bp = Blueprint('skills', __name__)

# Dependency injection for the service layer
def get_skills_service():
    db_session: Session = SessionLocal()
    return SkillsService(db_session)

@skills_bp.route('/addSkill', methods=['POST'])
def add_skill():
    try:
        data = request.json
        consultant_id = data.get('consultant_id')
        technologies_known = data.get('technologies_known')
        years_of_experience = data.get('years_of_experience')
        strength_of_skill = data.get('strength_of_skill')
        if not all([consultant_id, technologies_known, years_of_experience, strength_of_skill]):
            return jsonify({'error': 'Missing required fields'}), 400
        skills_service = get_skills_service()
        skill = skills_service.add_skill(consultant_id, technologies_known, years_of_experience, strength_of_skill)
        return jsonify({'success': True, 'skill_id': skill.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/getSkill/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
    try:
        skills_service = get_skills_service()
        skill = skills_service.get_skill(skill_id)
        if not skill:
            return jsonify({'error': 'Skill not found'}), 404
        return jsonify({
            'id': skill.id,
            'consultant_id': skill.consultant_id,
            'technologies_known': skill.technologies_known,
            'years_of_experience': skill.years_of_experience,
            'strength_of_skill': skill.strength_of_skill
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/getSkillsByConsultant/<int:consultant_id>', methods=['GET'])
def get_skills_by_consultant(consultant_id):
    try:
        skills_service = get_skills_service()
        skills = skills_service.get_skills_by_consultant(consultant_id)
        return jsonify([
            {
                'id': skill.id,
                'consultant_id': skill.consultant_id,
                'technologies_known': skill.technologies_known,
                'years_of_experience': skill.years_of_experience,
                'strength_of_skill': skill.strength_of_skill
            } for skill in skills
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/getAllSkills', methods=['GET'])
def get_all_skills():
    try:
        skills_service = get_skills_service()
        skills = skills_service.get_all_skills()
        return jsonify([
            {
                'id': skill.id,
                'consultant_id': skill.consultant_id,
                'technologies_known': skill.technologies_known,
                'years_of_experience': skill.years_of_experience,
                'strength_of_skill': skill.strength_of_skill
            } for skill in skills
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/updateSkill/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    try:
        data = request.json
        skills_service = get_skills_service()
        skill = skills_service.update_skill(skill_id, **data)
        if not skill:
            return jsonify({'error': 'Skill not found'}), 404
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/deleteSkill/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    try:
        skills_service = get_skills_service()
        success = skills_service.delete_skill(skill_id)
        if not success:
            return jsonify({'error': 'Skill not found'}), 404
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@skills_bp.route('/getSkillsByEmpId/<emp_id>', methods=['GET'])
def get_skills_by_emp_id(emp_id):
    try:
        skills_service = get_skills_service()
        skills = skills_service.get_skills_by_emp_id(emp_id)
        return jsonify([
            {
                'id': skill.id,
                'consultant_id': skill.consultant_id,
                'technologies_known': skill.technologies_known,
                'years_of_experience': skill.years_of_experience,
                'strength_of_skill': skill.strength_of_skill
            } for skill in skills
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
