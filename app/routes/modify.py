import os, uuid
from datetime import datetime
from flask import (
    Blueprint, 
    request,
    render_template, 
    redirect, 
    url_for, 
    flash,  
    current_app as app
)
from werkzeug.utils import secure_filename
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import *

bp = Blueprint("modify", __name__)

@bp.route("/upload/photos/<int:id>", methods=["GET", "POST"])
def upload_photos(id):
    if request.method == "POST":
            try:
                foto = request.files.getlist("foto")

                for file in foto:
                    if file and file.filename:
                        file_name = secure_filename(f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}")
                        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
                        file.save(file_path)

                        new_foto = FotoUS(
                            id_scheda_us=id,
                            filename=file_name
                        )

                        db.session.add(new_foto)
            except Exception as e:
                db.session.rollback()
                flash(f"Errore durante il caricamento del file: {str(e)}", "error")
                return redirect(url_for("modify.upload_photos", id=id))
            
            db.session.commit()
            flash(f"Foto caricate con successo!", "success")
            return redirect(url_for("view.scheda", id=id))
            
    return render_template("upload/photos.html", id=id)