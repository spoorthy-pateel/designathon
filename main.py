from flask import Flask
from controllers.user_controller import user_bp
from controllers.consultant_controller import consultant_bp
from database import init_db

app = Flask(__name__)

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(consultant_bp,url_prefix='/consultant')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
