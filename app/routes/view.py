from flask import Blueprint, render_template
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from models import *

bp = Blueprint("view", __name__)

@bp.route("/manuale", methods=["GET"])
def visualizza_manuale():
    return render_template("view/manuale.html")

@bp.route("/visualizza_anagrafiche", methods=["GET"])
def visualizza_anagrafiche():
    records = Anagrafica.query.order_by(Anagrafica.cognome.asc()).all()
    return render_template("view/visualizza_anagrafiche.html", records=records)


@bp.route("/visualizza_localita", methods=["GET"])
def visualizza_localita():
    records = Localita.query.all()
    return render_template("view/visualizza_localita.html", records=records)


@bp.route("/visualizza_enti", methods=["GET"])
def visualizza_enti():
    records = Ente.query.order_by(Ente.nome.asc()).all()
    return render_template("view/visualizza_enti.html", records=records)


@bp.route("/visualizza_schede", methods=["GET"])
def visualizza_schede():
    records = ModSchedaUs.query.order_by(ModSchedaUs.num_us.asc()).all()
    return render_template("view/visualizza_schede.html", records=records)