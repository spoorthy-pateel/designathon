from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import importlib
import pdfplumber
import json
import re
from OpenRouter import openrouter_chat
from resume_database import insert_resume_data
from controllers.user_controller import user_bp
from controllers.training_controller import training_bp
from controllers.consultant_training_controller import consultant_training_bp
from controllers.consultant_controller import consultant_bp
# SQLAlchemy database setup
from database import init_db


app = Flask(__name__)
CORS(app)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(consultant_bp,url_prefix='/consultant')

app.register_blueprint(training_bp, url_prefix='/training')

app.register_blueprint(consultant_training_bp,url_prefix='/consultantTraining')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def clean_llm_json(content):
    # Remove code fences and leading/trailing whitespace
    content = re.sub(r"^```json|^```|```$", "", content.strip(), flags=re.MULTILINE).strip()
    return content

@app.route('/api/agent/<agent_name>', methods=['POST'])
def agent_handler(agent_name):
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        resume_text = extract_text_from_pdf(filepath)

        # Dynamically import the agent module
        try:
            agent_module = importlib.import_module(f"agents.{agent_name}")
            prompt = agent_module.build_prompt(resume_text)
        except ModuleNotFoundError:
            return jsonify({'error': f'Agent \"{agent_name}\" not found.'}), 400

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

            # Insert into database with SQLAlchemy session!
            db = SessionLocal()
            insert_resume_data(data, user_id=1, db_session=db)  # Change user_id logic as needed
            db.close()

            return jsonify({'success': True, 'data': data})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed, only PDF supported'}), 400

if __name__ == "__main__":
    init_db()
    app.run(debug=True)