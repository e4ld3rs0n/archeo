from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for, flash, render_template_string
from sqlalchemy import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import *

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    if not tables:
        # No tables exist — needs initialization
        flash("Attenzione: il database è vuoto. Prima di continuare è necessario inizializzarlo.", "warning")
        return render_template("setup/setup.html")

    return render_template("index.html")

@bp.route("/initdb", methods=["GET"])
def initdb():
    print("HIT /initdb")
    try:
        db.create_all()
    except Exception as e:
        flash(f"Errore durante la creazione del database: {str(e)}", "error")
        return redirect(url_for("main.index"))
    
    flash("Database inizializzato con successo!", "success")
    return redirect(url_for("main.index"))

@bp.route("/dumpdb")
def dumpdb():
    inspector = inspect(db.engine)
    output = ""

    for table_name in inspector.get_table_names():
        output += f"<h2>Table: {table_name}</h2><table border=1><tr>"
        
        # Get column names
        columns = [col["name"] for col in inspector.get_columns(table_name)]
        output += "".join(f"<th>{col}</th>" for col in columns)
        output += "</tr>"

        # Get data
        result = db.session.execute(text(f"SELECT * FROM {table_name}")).fetchall()
        for row in result:
            output += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
        output += "</table><br>"

    return render_template_string(output)

@bp.route("/ente", methods=["GET", "POST"])
def ente():
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
        return redirect(url_for("main.ente"))
    
    lista_localita=Localita.query.all()
    
    return render_template("ente.html", lista_localita=lista_localita)

@bp.route("/scheda", methods=["GET", "POST"])
def scheda():
    print("HIT /scheda")

    if request.method == "POST":
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
                path_foto = request.form.get("path_foto"),
                path_ortofoto = request.form.get("path_ortofoto")
            )

            db.session.add(new_scheda)
            db.session.commit()
            flash("Scheda US creata!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Errore nella creazione: {str(e)}", "error")

        return redirect(url_for("main.scheda"))

    anagrafica = Anagrafica.query.all()
    enti = Ente.query.all()
    localita = Localita.query.all()
    schede = ModSchedaUs.query.order_by(ModSchedaUs.id.desc()).all()

    return render_template(
        "scheda.html",
        anagrafica=anagrafica,
        enti=enti,
        localita=localita,
        schede=schede
    )

@bp.route("/sequenza_fisica", methods=["GET", "POST"])
def sequenza_fisica():
    print("HIT /sequenza_fisica")

    if request.method == "POST":
        try:
            seq_a = request.form.get("id_seq_a")
            seq_b = request.form.get("id_seq_b")
            
            # Check if seq_a is equal to seq_b
            if seq_a == seq_b:
                flash(f"Errore: la sequenza A non può essere uguale alla sequenza B!", "error")
                return redirect(url_for("main.sequenza_fisica"))
            
            # Check if the sequence already exists
            existing_seq = SeqFisica.query.filter_by(id_seq_a=seq_a, id_seq_b=seq_b).first()
            if existing_seq:
                flash(f"Errore: questa sequenza fisica esiste già!", "error")
                return redirect(url_for("main.sequenza_fisica"))

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
        return redirect(url_for("main.sequenza_fisica"))

    # Fetch existing data for the form
    schede = ModSchedaUs.query.all()

    return render_template(
        "sequenza_fisica.html",
        schede=schede
    )

@bp.route("/sequenza_stratigrafica", methods=["GET", "POST"])
def sequenza_stratigrafica():
    print("HIT /sequenza_stratigrafica")

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
                return redirect(url_for("main.sequenza_fisica"))
            
            # Check if the sequence already exists
            existing_seq = SeqStrat.query.filter_by(id_seq_a=seq_a, id_seq_b=seq_b).first()
            if existing_seq:
                flash(f"Errore: questa sequenza stratigrafica esiste già!", "error")
                return redirect(url_for("main.sequenza_stratigrafica"))

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
        return redirect(url_for("main.sequenza_stratigrafica"))

    # Fetch existing data for the form
    schede = ModSchedaUs.query.all()

    return render_template(
        "sequenza_stratigrafica.html",
        schede=schede
    )

@bp.route("/scheda/<int:id>")
def visualizza_scheda(id):
    # Fetch the scheda by ID
    scheda = ModSchedaUs.query.get(id)
    if scheda is None:
        flash("Scheda non trovata", "error")
        return redirect(url_for("main.scheda"))

    rel_partenza = SeqFisica.query.filter(SeqFisica.id_seq_a == id).all()
    rel_arrivo = SeqFisica.query.filter(SeqFisica.id_seq_b == id).all()
    rel_strat_partenza = SeqStrat.query.filter(SeqStrat.id_seq_a == id).all()
    rel_strat_arrivo = SeqStrat.query.filter(SeqStrat.id_seq_b == id).all()

    return render_template(
        "view_scheda.html", 
        scheda=scheda, 
        rel_partenza=rel_partenza, 
        rel_arrivo=rel_arrivo,
        rel_strat_partenza=rel_strat_partenza,
        rel_strat_arrivo=rel_strat_arrivo
    )










@bp.route("/create-dummy-data")
def create_dummy_data():
    try:
        
        # Clear existing data if needed
        # db.session.query(ModSchedaUs).delete()
        # db.session.query(Ente).delete()
        # db.session.query(Localita).delete()
        # db.session.query(Anagrafica).delete()

        # Create dummy people
        person1 = Anagrafica(nome="Mario", cognome="Rossi", email="mario.rossi@example.com", tel="1234567890")
        person2 = Anagrafica(nome="Luigi", cognome="Verdi", email="luigi.verdi@example.com", tel="0987654321")
        person3 = Anagrafica(nome="Giulia", cognome="Bianchi", email="giulia.bianchi@example.com", tel="3345566778")
        person4 = Anagrafica(nome="Marco", cognome="Neri", email="marco.neri@example.com", tel="3471122334")
        person5 = Anagrafica(nome="Sara", cognome="Conti", email="sara.conti@example.com", tel="3668899001")

        # Create dummy locations
        loc1 = Localita(denom="Sito Archeologico A", via="Via Roma 1", citta="Roma", provincia="RM", cap="00100")
        loc2 = Localita(denom="Museo Nazionale", via="Corso Italia 22", citta="Milano", provincia="MI", cap="20100")
        loc3 = Localita(denom="Parco Storico", via="Via Garibaldi 10", citta="Torino", provincia="TO", cap="10100")
        loc4 = Localita(denom="Area Scavi", via="Piazza Dante 5", citta="Napoli", provincia="NA", cap="80100")

        # Create dummy ente
        ente1 = Ente(nome="Soprintendenza Archeologia Roma", tel="0654321987", email="info@ente1.it", localita=loc1)
        ente2 = Ente(nome="Soprintendenza Archeologia Parma", tel="4589321987", email="info@ente2.it", localita=loc2)

        db.session.add_all([person1, person2, person3, person4, person5, loc1, loc2, loc3, loc4, ente1, ente2])
        db.session.commit()

        # Create dummy dataset
        schede = []
        for i in range(1, 12):
            scheda = ModSchedaUs(
                num_us=str(i*100),
                id_responsabile=person1.id,
                id_res_scientifico=person2.id,
                descrizione=f"Descrizione della scheda {i}",
                id_ente_resp=ente1.id,
                id_localita=loc1.id,
                data=datetime.utcnow(),
                quadrato=f"B{i}",
                colore="Marrone",
                composizione="Terra",
                consistenza="Media",
                comp_organici="Carboni",
                comp_inorganici="Mattoni",
                interpretazione="Strato abitativo",
                misure="1x1m",
                note="Nessuna nota rilevante",
                campionature=True if i % 2 == 0 else False,
                flottazione=False,
                setacciatura="2mm",
                affidabilita_strat="Buona",
                modo_formazione="Deposizione antropica",
                elem_datanti="Ceramica",
                path_foto=f"foto{i}.jpg",
                path_ortofoto=f"ortofoto{i}.jpg"
            )
            schede.append(scheda)

        db.session.add_all(schede)
        db.session.commit()

        return f"{len(schede)} schede create con successo."
    except Exception as e:
        db.session.rollback()
        return f"Errore durante la creazione dei dati: {str(e)}"