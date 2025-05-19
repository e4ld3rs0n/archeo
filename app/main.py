import os
from flask import Flask
from db import init_app
from models import *
from utils import bp
from routes.view import bp as view_bp
from routes.create import bp as create_bp
from routes.delete import bp as delete_bp
from routes.modify import bp as modify_bp
from routes.search import bp as search_bp
from routes.preferences import bp as preferences_bp
from utilities.preferences import init_preferences

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB
app.config["ALLOWED_IMAGE_EXTENSIONS"] = {"png", "jpg", "jpeg"}

app.secret_key = os.getenv("SECRET_KEY", "archeo_secret_key")

init_app(app)

init_preferences(app)                   # Initialize user preferences

app.register_blueprint(bp)              # Register the main blueprint
app.register_blueprint(view_bp)         # Register the view blueprint
app.register_blueprint(create_bp)       # Register the create blueprint
app.register_blueprint(delete_bp)       # Register the delete blueprint
app.register_blueprint(modify_bp)       # Register the modify blueprint
app.register_blueprint(search_bp)       # Register the search blueprint
app.register_blueprint(preferences_bp)  # Register the preferences blueprint

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)