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

bp = Blueprint("create", __name__)

@bp.route("/crea/anagrafica", methods=["GET", "POST"])
def nuova_anagrafica():
        if request.method == "POST":
            try:
                nome = request.form.get("nome")
                if not nome:
                    flash("Il nome è obbligatorio!", "error")
                    return redirect(url_for("create.nuova_anagrafica"))

                cognome = request.form.get("cognome")
                if not cognome:
                    flash("Il cognome è obbligatorio!", "error")
                    return redirect(url_for("create.nuova_anagrafica"))
                
                email = request.form.get("email")
                if not email:
                    flash("L'indirizzo e-mail è obbligatorio!", "error")
                    return redirect(url_for("create.nuova_anagrafica"))

                tel = request.form.get("tel")
                if not tel:
                    flash("Il telefono è obbligatorio!", "error")
                    return redirect(url_for("create.nuova_anagrafica"))

                new_anagrafica = Anagrafica(
                    nome=nome,
                    cognome=cognome,
                    email=email,
                    tel=tel
                )

                db.session.add(new_anagrafica)
                db.session.commit()

                flash(f"Anagrafica per {nome} {cognome} creata!", "success")
                return redirect(url_for("create.nuova_anagrafica"))
            except Exception as e:
                db.session.rollback()
                flash(f"Errore nella creazione: {str(e)}", "error")
    
        return render_template("anagrafica.html")

@bp.route("/crea/localita", methods=["GET", "POST"])
def nuova_localita():
    if request.method == "POST":
        try:
            denominazione = request.form.get("denominazione")
            via = request.form.get("via")
            if not via:
                flash("La via è obbligatoria!", "error")
                return redirect(url_for("create.nuova_localita"))

            citta = request.form.get("citta")
            if not citta:
                flash("La città è obbligatoria!", "error")
                return redirect(url_for("create.nuova_localita"))

            provincia = request.form.get("provincia")
            if not provincia:
                flash("La provincia è obbligatoria!", "error")
                return redirect(url_for("create.nuova_localita"))
            
            cap = request.form.get("cap")
            if not cap:
                flash("Il CAP è obbligatorio!", "error")
                return redirect(url_for("create.nuova_localita"))

            new_localita = Localita(
                denom=denominazione,
                via=via,
                citta=citta,
                provincia=provincia,
                cap=cap
            )

            db.session.add(new_localita)
            db.session.commit()

            flash(f"Nuova località in {via} {citta} ({provincia}) creata!", "success")
            return redirect(url_for("create.nuova_localita"))
        except Exception as e:
            db.session.rollback()
            flash(f"Errore nella creazione: {str(e)}", "error")
    
    return render_template("localita.html")

@bp.route("/crea/us", methods=["GET", "POST"])
def nuova_scheda_us():
    if request.method == "POST":
        # Create the US model
        try:
            unique_num_us = request.form.get("num_us")
            # Ensure num_us is unique
            test = ModSchedaUs.query.filter_by(num_us=unique_num_us).first()
            if test: 
                flash(f"Errore: il numero US {unique_num_us} esiste già!", "error")
                return redirect(url_for("main.scheda"))
            
            new_scheda = ModSchedaUs(
                num_us = unique_num_us,
                id_responsabile = request.form.get("id_responsabile"),
                id_res_scientifico = request.form.get("id_res_scientifico"),
                descrizione = request.form.get("descrizione"),
                id_ente_resp = request.form.get("id_ente_resp"),
                id_localita = request.form.get("id_localita"),
                data = datetime.strptime(request.form.get("data"), "%Y-%m-%d"),
                quadrato = request.form.get("quadrato"),
                colore = request.form.get("colore"),
                composizione = request.form.get("composizione"),
                consistenza = request.form.get("consistenza"),
                comp_organici = request.form.get("comp_organici"),
                comp_inorganici = request.form.get("comp_inorganici"),
                interpretazione = request.form.get("interpretazione"),
                misure = request.form.get("misure"),
                note = request.form.get("note"),
                campionature = bool(request.form.get("campionature")),
                flottazione = bool(request.form.get("flottazione")),
                setacciatura = request.form.get("setacciatura"),
                affidabilita_strat = request.form.get("affidabilita_strat"),
                modo_formazione = request.form.get("modo_formazione"),
                elem_datanti = request.form.get("elem_datanti"),
            )

            db.session.add(new_scheda)
            db.session.commit()
            flash("Scheda US creata!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Errore nella creazione: {str(e)}", "error")

            # If the creation fails, redirect to the previous page without processing the photos
            return redirect(url_for("create.nuova_scheda_us"))

        # Handle photo upload
        try:
            # Obtain uploaded files
            foto = request.files.getlist("foto")
            piante = request.files.getlist("pianta")
            ortofoto = request.files.getlist("ortofoto")

            # Process each file
            for file in foto:
                if file and file.filename:
                    file_name = secure_filename(f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}")
                    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
                    file.save(file_path)

                    new_foto = FotoUS(
                        id_mod_scheda_us=new_scheda.id,
                        filename=file_name
                    )

                    db.session.add(new_foto)
                    db.session.commit()
                    flash(f"Foto {file_name} caricata!", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Errore nel caricamento dei file: {str(e)}", "error")

        return redirect(url_for("view.scheda", id=new_scheda.id))

    anagrafica = Anagrafica.query.all()
    enti = Ente.query.all()
    localita = Localita.query.all()
    schede = ModSchedaUs.query.order_by(ModSchedaUs.id.desc()).all()

    return render_template(
        "create/nuova_scheda.html",
        anagrafica=anagrafica,
        enti=enti,
        localita=localita,
        schede=schede
    )

@bp.route("/seq_fisica", methods=["GET", "POST"])
def nuova_sequenza_fisica():

    if request.method == "POST":
        try:
            seq_a = request.form.get("id_seq_a")
            seq_b = request.form.get("id_seq_b")
            
            # Check if seq_a is equal to seq_b
            if seq_a == seq_b:
                flash(f"Errore: la sequenza A non può essere uguale alla sequenza B!", "error")
                return redirect(url_for("create.nuova_sequenza_fisica"))
            
            # Check if the sequence already exists
            existing_seq = SeqFisica.query.filter_by(id_seq_a=seq_a, id_seq_b=seq_b).first()
            if existing_seq:
                flash(f"Errore: questa sequenza fisica esiste già!", "error")
                return redirect(url_for("create.nuova_sequenza_fisica"))

            # Proceed with adding the new sequence
            new_seq_fisica = SeqFisica(
                id_seq_a = seq_a,
                id_seq_b = seq_b,
                sequenza = request.form.get("sequenza")
            )

            db.session.add(new_seq_fisica)
            db.session.commit()
            flash("Sequenza fisica creata!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Errore nella creazione: {str(e)}", "error")
        return redirect(url_for("create.nuova_sequenza_fisica"))

    # Fetch existing data for the form
    schede = ModSchedaUs.query.all()

    return render_template(
        "create/sequenza_fisica.html",
        schede=schede
    )

@bp.route("/seq_stratigrafica", methods=["GET", "POST"])
def nuova_sequenza_stratigrafica():

    if request.method == "POST":
        try:
            
            seq = request.form.get("sequenza")
            if seq == "posteriore_a":
                seq_a = request.form.get("id_seq_a")
                seq_b = request.form.get("id_seq_b")
            else:
                seq_a = request.form.get("id_seq_b")
                seq_b = request.form.get("id_seq_a")
            
            # Check if seq_a is equal to seq_b
            if seq_a == seq_b:
                flash(f"Errore: la sequenza A non può essere uguale alla sequenza B!", "error")
                return redirect(url_for("create.nuova_sequenza_stratigrafica"))
            
            # Check if the sequence already exists
            existing_seq = SeqStrat.query.filter_by(id_seq_a=seq_a, id_seq_b=seq_b).first()
            if existing_seq:
                flash(f"Errore: questa sequenza stratigrafica esiste già!", "error")
                return redirect(url_for("create.nuova_sequenza_stratigrafica"))

            # Proceed with adding the new sequence
            new_seq_strat = SeqStrat(
                id_seq_a = seq_a,
                id_seq_b = seq_b,
            )

            db.session.add(new_seq_strat)
            db.session.commit()
            flash("Sequenza stratigrafica creata!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Errore nella creazione: {str(e)}", "error")
        return redirect(url_for("create.nuova_sequenza_stratigrafica"))

    # Fetch existing data for the form
    schede = ModSchedaUs.query.all()

    return render_template(
        "create/sequenza_stratigrafica.html",
        schede=schede
    )