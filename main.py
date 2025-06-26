from flask import Flask
from controllers.user_controller import user_bp
from controllers.training_controller import training_bp
from controllers.consultant_training_controller import consultant_training_bp


app = Flask(__name__)

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')

app.register_blueprint(training_bp, url_prefix='/training')

app.register_blueprint(consultant_training_bp,url_prefix='/consultantTraining')

if __name__ == "__main__":
    app.run(debug=True)




