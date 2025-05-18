import os, uuid
from datetime import datetime, date
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

@bp.route("/crea/ente", methods=["GET", "POST"])
def nuovo_ente():
    print ("HIT /ente")

    if request.method == "POST":
        nome = request.form.get("nome")
        if not nome:
            flash("Il nome dell'ente è obbligatorio!", "error")
            return redirect(url_for("main.ente"))

        tel = request.form.get("tel")
        email = request.form.get("email")
        id_loc = request.form.get("id_loc")

        new_ente = Ente(
            id_loc = id_loc,
            nome = nome,
            tel = tel,
            email = email
        )

        db.session.add(new_ente)
        db.session.commit()

        flash(f"Ente creato!", "success")
        return redirect(url_for("view.visualizza_enti"))
    
    lista_localita=Localita.query.all()
    
    return render_template("ente.html", lista_localita=lista_localita)

@bp.route("/crea/us", methods=["GET", "POST"])
def nuova_scheda_us():
    if request.method == "POST":
        # Create the US model
        try:
            unique_num_us = request.form.get("num_us")
            
            # Ensure num_us is unique in the database
            test_us = SchedaUS.query.filter_by(num_us=unique_num_us).first()
            if test_us: 
                flash(f"Errore: il numero US {unique_num_us} esiste già!", "error")
                return redirect(url_for("create.nuova_scheda_us"))
            
            pianta = request.files.get("pianta")
            pianta_filename = secure_filename(f"{uuid.uuid4().hex}{os.path.splitext(pianta.filename)[1]}")
            pianta_path = os.path.join(app.config["UPLOAD_FOLDER"], pianta_filename)
            
            try:
                pianta.save(pianta_path)
            except Exception as e:
                flash(f"Errore nel caricamento della pianta: {str(e)}", "error")
                pianta_filename = None

            new_scheda = SchedaUS(
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
                flottazione = request.form.get("flottazione"),
                setacciatura = request.form.get("setacciatura"),
                affidabilita_strat = request.form.get("affidabilita_strat"),
                modo_formazione = request.form.get("modo_formazione"),
                elem_datanti = request.form.get("elem_datanti"),
                settore = request.form.get("settore"),
                stato_conservazione = request.form.get("stato_conservazione"),
                def_e_pos = request.form.get("def_e_pos"),
                criteri_distinzione = request.form.get("criteri_distinzione"),
                pianta_filename = pianta_filename
            )

            db.session.add(new_scheda)
        except Exception as e:
            db.session.rollback()
            flash(f"Errore nella creazione: {str(e)}", "error")

            # If the creation fails, redirect to the previous page without processing the photos
            return redirect(url_for("create.nuova_scheda_us"))

        db.session.commit()
        flash("Scheda US creata", "success")

        # Handle photo upload
        try:
            # Obtain uploaded photos
            foto = request.files.getlist("foto")
            
            # Process each photo
            for file in foto:
                if file and file.filename:
                    file_name = secure_filename(f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}")
                    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
                    file.save(file_path)

                    new_foto = FotoUS(
                        id_scheda_us=new_scheda.id,
                        filename=file_name
                    )

                    db.session.add(new_foto)

        except Exception as e:
            db.session.rollback()
            flash(f"Errore nel caricamento dei file: {str(e)}", "error")

        db.session.commit()
        return redirect(url_for("view.scheda", id=new_scheda.id))

    anagrafica = Anagrafica.query.all()
    enti = Ente.query.all()
    localita = Localita.query.all()
    schede = SchedaUS.query.order_by(SchedaUS.id.desc()).all()
    today_date = date.today().strftime('%Y-%m-%d')

    return render_template(
        "create/nuova_scheda.html",
        today_date=today_date,
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
    schede = SchedaUS.query.order_by(SchedaUS.id).all()

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
    schede = SchedaUS.query.order_by(SchedaUS.id).all()

    return render_template(
        "create/sequenza_stratigrafica.html",
        schede=schede
    )

@bp.route("/reperto_notevole", methods=["GET", "POST"])
def nuovo_reperto_notevole():
    if request.method == "POST":
        try:
            new_reperto = RepertoNotevoleUS(
                id_scheda_us = request.form.get("id_scheda"),
                numero_cassa = request.form.get("numero_cassa"),
                sito = request.form.get("sito"),
                data = datetime.strptime(request.form.get("data"), "%Y-%m-%d"),
                materiale = request.form.get("materiale"),
                descrizione = request.form.get("descrizione"),
                quantita = request.form.get("quantita"),
                lavato = bool(request.form.get("lavato")),
                siglato = bool(request.form.get("siglato")),
                punto_stazione_totale = request.form.get("punto_stazione_totale"),
                coord_y = request.form.get("coord_y"),
                coord_x = request.form.get("coord_x"),
                coord_z = request.form.get("coord_z"),
                note = request.form.get("note")
            )
        
            db.session.add(new_reperto)
        except Exception as e:
            db.session.rollback()
            flash(f"Errore nella creazione: {str(e)}", "error")
            return redirect(url_for("create.nuovo_reperto_notevole"))

        db.session.commit()
        flash("Reperto notevole creato!", "success")

    # Fetch existing data for the form
    schede = SchedaUS.query.order_by(SchedaUS.id).all()
    today_date = date.today().strftime('%Y-%m-%d')

    return render_template(
        "create/nuovo_reperto_notevole.html",
        today_date=today_date,
        schede=schede
    )

@bp.route("/nuova_ortofoto", methods=["GET", "POST"])
def nuova_ortofoto():
    if request.method == "POST":
        try:
            # Crea il record per l'ortofoto nel database
            new_ortofoto = Ortofoto(
                id_operatore=request.form.get("id_operatore"),
                descrizione=request.form.get("descrizione"),
                data = datetime.strptime(request.form.get("data"), "%Y-%m-%d"),
                target=request.form.get("target"),
                note=request.form.get("note"),
                path_ortofoto=request.form.get("path_ortofoto"),
                completato = True if request.form.get("completato") == "si" else False
            )

            db.session.add(new_ortofoto)
            db.session.flush()  # Assigns new_ortofoto.id without committing

            # Associa l'ortofoto alle US indicate rimuovendo i duplicati
            schede_us_associate = list(set(request.form.getlist('schede_us')))
            
            for scheda_id in schede_us_associate:
                if scheda_id != "null":
                    scheda = SchedaUS.query.get(int(scheda_id))
                    if scheda:
                        if scheda.id_ortofoto is None:
                            scheda.id_ortofoto = new_ortofoto.id
                        else:
                            flash(f"La scheda US {scheda.num_us} ha già una ortofoto associata", "warning")
                    else:
                        flash(f"La scheda selezionata con ID {scheda_id} non esiste nel database", "warning")

        except Exception as e:
            db.rollback()
            flash(f"Errore: {str(e)}", "error")
            return redirect(url_for("create.nuova_ortofoto"))
        
        db.session.commit()
        flash("Ortofoto creata", "success")

    schede = SchedaUS.query.order_by(SchedaUS.id).all()
    anagrafiche = Anagrafica.query.all()
    today_date = date.today().strftime('%Y-%m-%d')

    return render_template(
        "create/nuova_ortofoto.html",
        today_date=today_date,
        anagrafiche=anagrafiche,
        schede=schede
    )