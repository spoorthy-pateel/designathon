import pdfplumber
import json
from flask import jsonify
from OpenRouter import openrouter_chat
from resume_database import insert_resume_data
from database import SessionLocal
import re
import os

try:
    import docx  # python-docx
except ImportError:
    docx = None

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(filepath):
    if docx is None:
        raise ImportError("python-docx is not installed. Please install it with `pip install python-docx`.")
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext == ".docx":
        return extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file type: only PDF and DOCX are supported.")

def build_prompt(resume_text):
    return f"""
IMPORTANT: Respond ONLY with a valid JSON object. 
NO markdown, NO code fences, NO explanations, NO comments, NO extra text.
If you include anything other than the JSON object, the result will be discarded.

Output must be a pure JSON object matching this structure:
{{
  "skills": [
    {{
      "technologies_known": "string (e.g., Python, JavaScript, etc.)",
      "years_of_experience": number (e.g., 3.5),
      "strength_of_skill": integer (1-5, how strong this skill is based on the resume)
    }}
  ],
  "certifications": [
    {{
      "certification_name": "string",
      "issued_date": "YYYY-MM-DD",
      "valid_till": "YYYY-MM-DD or null"
    }}
  ],
  "professional": {{
    "last_worked_organization": "string",
    "recent_role": "string",
    "recent_project": "string or null",
    "recent_start_date": "YYYY-MM-DD or null",
    "recent_project_release_date": "YYYY-MM-DD or null"
  }}
}}

Guidelines:
- Estimate years_of_experience as accurately as possible from the resume.
- For strength_of_skill, give an integer 1 (weakest) to 10 (strongest) for each skill, based on emphasis and context.
- Use ISO 8601 date format (YYYY-MM-DD) for all dates.
- If any information is missing, set its value to null.

Resume Text:
\"\"\"
{resume_text}
\"\"\"
"""

def clean_llm_json(content):
    content = re.sub(r"^```json|^```|```$", "", content.strip(), flags=re.MULTILINE).strip()
    return content

def handle_request(request, context):
    upload_path = context.get("upload_path")
    if not upload_path:
        return jsonify({"error": "No resume file uploaded (PDF or DOCX)"}), 400

    emp_id = request.headers.get("X-Emp-ID")
    if not emp_id:
        return jsonify({"error": "Missing emp_id in request header"}), 400

    try:
        resume_text = extract_text_from_file(upload_path)
    except Exception as e:
        return jsonify({"error": f"Failed to extract text: {str(e)}"}), 400

    print(resume_text)

    prompt = build_prompt(resume_text)

    try:
        llm_response = openrouter_chat(prompt)
        content = (
            llm_response.get('choices', [{}])[0].get('message', {}).get('content', '')
            or llm_response.get('content', '')
        )
        try:
            data = json.loads(clean_llm_json(content))
        except Exception as e:
            return jsonify({'error': 'LLM output was not valid JSON', 'llm_content': content}), 500

        db = SessionLocal()
        insert_resume_data(data, emp_id=emp_id, db_session=db)
        db.close()

        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
