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
    page_title = "Manuale"

    return render_template("view/manuale.html", title=page_title)

@bp.route("/visualizza_anagrafiche", methods=["GET"])
def visualizza_anagrafiche():
    page_title = "Anagrafiche"

    records = Anagrafica.query.order_by(Anagrafica.cognome.asc()).all()
    return render_template("view/visualizza_anagrafiche.html", records=records, title=page_title)

@bp.route("/visualizza_localita", methods=["GET"])
def visualizza_localita():
    page_title = "Località"

    records = Localita.query.all()
    return render_template("view/visualizza_localita.html", records=records, title=page_title)

@bp.route("/visualizza_enti", methods=["GET"])
def visualizza_enti():
    page_title = "Enti"

    records = Ente.query.order_by(Ente.nome.asc()).all()
    return render_template("view/visualizza_enti.html", records=records, title=page_title)

@bp.route("/visualizza_schede", methods=["GET"])
def visualizza_schede():
    page_title = "Schede US"

    records = SchedaUS.query.order_by(SchedaUS.num_us.asc()).all()
    return render_template("view/visualizza_schede.html", records=records, title=page_title)

@bp.route("/scheda/<int:id>")
def scheda(id):
    # Fetch the scheda by ID
    scheda = SchedaUS.query.get(id)

    if scheda is None:
        flash("Scheda non trovata", "error")
        return redirect(url_for("main.scheda", title="Schede US"))

    rel_partenza = SeqFisica.query.filter(SeqFisica.id_seq_a == id).all()
    rel_arrivo = SeqFisica.query.filter(SeqFisica.id_seq_b == id).all()
    rel_strat_partenza = SeqStrat.query.filter(SeqStrat.id_seq_a == id).all()
    rel_strat_arrivo = SeqStrat.query.filter(SeqStrat.id_seq_b == id).all()

    foto = FotoUS.query.filter_by(id_scheda_us=id).all()
    reperti_notevoli = RepertoNotevoleUS.query.filter_by(id_scheda_us=id).all()

    page_title = f"Scheda US {scheda.num_us}"

    return render_template(
        "view/scheda_us.html", 
        scheda=scheda, 
        rel_partenza=rel_partenza, 
        rel_arrivo=rel_arrivo,
        rel_strat_partenza=rel_strat_partenza,
        rel_strat_arrivo=rel_strat_arrivo,
        foto=foto,
        reperti_notevoli=reperti_notevoli,
        title=page_title
    )

@bp.route("/visualizza_reperti_notevoli", methods=["GET"])
def visualizza_reperti_notevoli():
    page_title = "Reperti notevoli"

    reperti_notevoli = RepertoNotevoleUS.query.order_by(RepertoNotevoleUS.id_scheda_us.asc()).all()
    return render_template("view/visualizza_reperti_notevoli.html", reperti_notevoli=reperti_notevoli, title=page_title)

@bp.route("/reperto_notevole/<int:id>")
def reperto_notevole(id):
    # Fetch the scheda by ID
    reperto = RepertoNotevoleUS.query.get(id)
    
    if reperto is None:
        flash("Reperto non trovato", "error")
        return redirect(url_for("view.visualizza_reperti_notevoli", title="Reperti notevoli"))

    page_title = f"Reperto №{reperto.id}"

    return render_template(
        "view/reperto_notevole.html", 
        reperto=reperto,
        title=page_title
    )

@bp.route("/get/<path:filename>")
def photo(filename):
    photo_dir = app.config["UPLOAD_FOLDER"]
    return send_from_directory(photo_dir, filename)

@bp.route("/visualizza_ortofoto", methods=["GET"])
def visualizza_ortofoto():
    page_title = "Ortofoto"

    ortofoto = Ortofoto.query.order_by(Ortofoto.id.asc()).all()
    return render_template("view/visualizza_ortofoto.html", ortofoto=ortofoto, title=page_title)