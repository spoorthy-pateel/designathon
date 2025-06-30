import json
from flask import jsonify
from OpenRouter import openrouter_chat
from database import SessionLocal
from models.consultant import Consultant
from models.opportunity import Opportunity
import traceback

def build_prompt(skills, opportunities):
    """
    Builds a prompt for the LLM that asks it to match the consultant's skills and experience
    to the available opportunities and recommend the best ones.
    """
    return f"""
IMPORTANT: Respond ONLY with a valid JSON array of integers (opportunity IDs). 
NO markdown, NO code fences, NO explanations, NO extra text.

The consultant's extracted skills and experience:
{json.dumps(skills, indent=2)}

The list of available opportunities (each item: id, name, skills_expected, years_of_experience_required, deadline):
{json.dumps(opportunities, indent=2)}

Instructions:
- Output a JSON array containing the ids of the best-matching opportunities for the consultant, sorted from best to least match.
- The array must look like: [3, 4, 5]
- Do not include any other text or structure.
"""

def handle_request(request, context):
    # Get emp_id from header
    emp_id = request.headers.get("X-Emp-ID")
    if not emp_id:
        return jsonify({"error": "Missing emp_id in request header"}), 400

    db = SessionLocal()
    try:
        # Fetch consultant by emp_id
        consultant = db.query(Consultant).filter_by(emp_id=emp_id).first()
        if not consultant:
            return jsonify({"error": f"No consultant found with emp_id {emp_id}"}), 404

        # Extract consultant skills and experience
        # This assumes you have a Consultant.skills relationship and each Skill has .technologies_known, .years_of_experience, etc.
        skills = [
            {
                "technologies_known": skill.technologies_known,
                "years_of_experience": skill.years_of_experience,
                "strength_of_skill": getattr(skill, "strength_of_skill", None)
            }
            for skill in getattr(consultant, "skills", [])
        ]

        # Compute max experience
        years_of_experience = max([s["years_of_experience"] for s in skills if s["years_of_experience"] is not None] or [0])

        # Fetch all opportunities
        opportunities = db.query(Opportunity).all()
        opportunity_list = [
            {
                "id": o.id,
                "name": o.name,
                "skills_expected": o.skills_expected,
                "years_of_experience_required": o.years_of_experience_required,
                "deadline": o.deadline.isoformat() if o.deadline else None
            }
            for o in opportunities
        ]

        if not skills or not opportunity_list:
            return jsonify({"matches": []})  # Nothing to match

        # Build prompt for LLM
        prompt = build_prompt(
            {
                "skills": skills,
                "years_of_experience": years_of_experience
            },
            opportunity_list
        )

        # Call LLM
        llm_response = openrouter_chat(prompt)
        content = (
            llm_response.get('choices', [{}])[0].get('message', {}).get('content', '')
            or llm_response.get('content', '')
        )

        try:
            matches = json.loads(content)
        except Exception as e:
            return jsonify({
                'error': 'LLM output was not valid JSON',
                'llm_content': content,
                'traceback': traceback.format_exc()
            }), 500

        return jsonify({'matches': matches})

    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500
    finally:
        db.close()