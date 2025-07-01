import json
import re
from flask import jsonify
from OpenRouter import openrouter_chat
from database import SessionLocal
from models.consultant import Consultant
from models.consultant_opportunity import ConsultantOpportunity
from models.opportunity import Opportunity
from models.training import Training
import traceback

def build_prompt(skills, applied_skills, trainings):
    skills_section = (
        json.dumps(skills, indent=2) if skills and isinstance(skills.get("skills"), list) else "No skills data available."
    )
    applied_skills_section = (
        json.dumps(applied_skills, indent=2) if applied_skills else "No applied jobs data available."
    )

    return f"""
IMPORTANT: Respond ONLY with a valid JSON array of integers (training IDs). 
NO markdown, NO code fences, NO explanations, NO extra text.

The consultant's extracted skills and experience:
{skills_section}

The skills required in jobs they've applied to:
{applied_skills_section}

The list of available trainings (each item: id, name, skills_covered, duration):
{json.dumps(trainings, indent=2)}

Instructions:
- Output a JSON array containing the ids of the best-matching trainings for the consultant, sorted from best to least match.
- The array must look like: [3, 4, 5]
- Recommend trainings that best close the skill gap between the consultant's current skills and those required in their applied jobs.
- If there is no skill or applied job information, recommend the most relevant or foundational trainings.
- Do not include any other text or structure.
"""

def extract_json_array(text):
    try:
        # Remove code fences if present
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL).strip()

        # Extract first JSON array in text
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print("Error parsing cleaned JSON:", e)
    return None

def handle_request(request, context):
    emp_id = request.headers.get("X-Emp-ID")
    if not emp_id:
        print("Error: Missing emp_id in request header")
        return jsonify({"error": "Missing emp_id in request header"}), 400

    db = SessionLocal()
    try:
        consultant = db.query(Consultant).filter_by(emp_id=emp_id).first()
        if not consultant:
            print(f"Error: No consultant found with emp_id {emp_id}")
            return jsonify({"error": f"No consultant found with emp_id {emp_id}"}), 404

        skills = [
            {
                "technologies_known": skill.technologies_known,
                "years_of_experience": skill.years_of_experience,
                "strength_of_skill": getattr(skill, "strength_of_skill", None)
            }
            for skill in getattr(consultant, "skills", [])
        ]
        years_of_experience = max([s["years_of_experience"] for s in skills if s["years_of_experience"] is not None] or [0])

        applied_opp_ids = [
            co.opportunity_id for co in db.query(ConsultantOpportunity).filter_by(consultant_id=consultant.id).all()
        ]
        applied_opps = db.query(Opportunity).filter(Opportunity.id.in_(applied_opp_ids)).all()
        applied_skills = [
            {
                "id": o.id,
                "name": o.name,
                "skills_expected": o.skills_expected,
                "years_of_experience_required": o.years_of_experience_required,
                "deadline": o.deadline.isoformat() if o.deadline else None
            }
            for o in applied_opps
        ]

        trainings = db.query(Training).all()
        trainings_list = [
            {
                "id": t.id,
                "name": t.training_name,
                "skills_covered": t.technologies_learnt,
                "level": t.level_of_training.value if hasattr(t.level_of_training, "value") else str(t.level_of_training),
                "duration": t.duration,
                "description": getattr(t, "description", None)
            }
            for t in trainings
        ]

        if not trainings_list:
            print("Info: trainings_list is empty. Returning empty matches.")
            return jsonify({"matches": []})

        prompt = build_prompt(
            {
                "skills": skills,
                "years_of_experience": years_of_experience
            },
            applied_skills,
            trainings_list
        )

        print("Prompt sent to LLM:\n", prompt)

        llm_response = openrouter_chat(prompt)
        print("LLM raw response:", llm_response)
        content = (
            llm_response.get('choices', [{}])[0].get('message', {}).get('content', '')
            or llm_response.get('content', '')
        )
        print("LLM content:", content)

        matches = extract_json_array(content)
        if matches is None:
            print("Error: LLM output did not contain a valid JSON array")
            return jsonify({
                'error': 'LLM output did not contain a valid JSON array',
                'llm_content': content
            }), 500

        return jsonify({'matches': matches})

    except Exception as e:
        print("Exception caught in handle_request:")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500
    finally:
        db.close()
