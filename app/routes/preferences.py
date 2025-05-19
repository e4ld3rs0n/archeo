import os, uuid, time
from datetime import datetime
from flask import (
    Blueprint, 
    request,
    render_template, 
    redirect, 
    url_for, 
    flash,
    session,
    current_app as app
)
from werkzeug.utils import secure_filename
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import *

bp = Blueprint("preferences", __name__)

@bp.route("/switch_default_view", methods=["GET"])
def switch_default_view():
    current = session.get("default_view", "card")
    session["default_view"] = "grid" if current == "card" else "card"
    
    next_url = request.referrer or url_for("main.index")
    return redirect(next_url)