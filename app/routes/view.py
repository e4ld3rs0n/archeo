import os
from flask import (
    Blueprint, 
    render_template, 
    flash, 
    redirect, 
    url_for, 
    send_from_directory, 
    current_app as app
)
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

@bp.route("/scheda/<int:id>")
def scheda(id):
    # Fetch the scheda by ID
    scheda = ModSchedaUs.query.get(id)
    if scheda is None:
        flash("Scheda non trovata", "error")
        return redirect(url_for("main.scheda"))

    rel_partenza = SeqFisica.query.filter(SeqFisica.id_seq_a == id).all()
    rel_arrivo = SeqFisica.query.filter(SeqFisica.id_seq_b == id).all()
    rel_strat_partenza = SeqStrat.query.filter(SeqStrat.id_seq_a == id).all()
    rel_strat_arrivo = SeqStrat.query.filter(SeqStrat.id_seq_b == id).all()

    foto = FotoUS.query.filter_by(id_mod_scheda_us=id).all()
    piante = PiantaUS.query.filter_by(id_mod_scheda_us=id).all()
    ortofoto = OrtofotoUS.query.filter_by(id_mod_scheda_us=id).all()

    return render_template(
        "view/scheda_us.html", 
        scheda=scheda, 
        rel_partenza=rel_partenza, 
        rel_arrivo=rel_arrivo,
        rel_strat_partenza=rel_strat_partenza,
        rel_strat_arrivo=rel_strat_arrivo,
        foto=foto,
        piante=piante,
        ortofoto=ortofoto
    )

@bp.route("/photo/<path:filename>")
def photo(filename):
    photo_dir = app.config["UPLOAD_FOLDER"]
    return send_from_directory(photo_dir, filename)