from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import importlib
from controllers.user_controller import user_bp
from controllers.training_controller import training_bp
from controllers.consultant_training_controller import consultant_training_bp
from controllers.consultant_controller import consultant_bp
from controllers.skills_controller import skills_bp
from controllers.opportunity_controller import opportunity_bp
from controllers.consultant_opportunity_controller import consultant_opportunity_bp
from database import init_db

app = Flask(__name__)
CORS(app,supports_credentials=True)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(consultant_bp, url_prefix='/consultant')
app.register_blueprint(training_bp, url_prefix='/training')
app.register_blueprint(consultant_training_bp, url_prefix='/consultantTraining')
app.register_blueprint(skills_bp, url_prefix='/skills')
app.register_blueprint(opportunity_bp, url_prefix='/opportunity')
app.register_blueprint(consultant_opportunity_bp, url_prefix='/consultantOpportunity')

CORS(app, resources={r"/*": {"origins": "*"}})


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf','docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/agent/<agent_name>', methods=['POST'])
def agent_handler(agent_name):
    """
    Dispatches to agent modules. Each agent must define a `handle_request(request, context)` function
    that returns a Flask response or data.
    """
    # Load the agent module
    try:
        agent_module = importlib.import_module(f"agents.{agent_name}")
    except ModuleNotFoundError:
        return jsonify({'error': f'Agent "{agent_name}" not found.'}), 400

    # File upload handling (if the agent needs it)
    uploaded_file = None
    if 'resume' in request.files and allowed_file(request.files['resume'].filename):
        uploaded_file = request.files['resume']
        # Optionally save to disk (if needed by agent)
        upload_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(upload_path)
    else:
        upload_path = None

    # Provide a context dict for agents (add more as needed)
    context = {
        "upload_path": upload_path,
        "uploaded_file": uploaded_file,
        "files": request.files,
        "form": request.form,
        "json": request.get_json(silent=True),
        "args": request.args,
    }

    # Each agent's `handle_request` function decides what it needs from request/context
    try:
        # Agent is responsible for its own input validation and response
        return agent_module.handle_request(request, context)
    except Exception as e:
        return jsonify({'error': f'Agent error: {str(e)}'}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True)