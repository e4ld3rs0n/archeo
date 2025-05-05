import os
from flask import Flask
from db import init_app
from models import *
from rt import bp
from routes.view import bp as view_bp
from routes.create import bp as create_bp
from routes.delete import bp as delete_bp

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

app.secret_key = "your_secret_key"
init_app(app)

app.register_blueprint(bp)
app.register_blueprint(view_bp)
app.register_blueprint(create_bp)
app.register_blueprint(delete_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)