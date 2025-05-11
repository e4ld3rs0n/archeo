from flask import Blueprint, render_template, redirect, url_for, flash, render_template_string
from sqlalchemy import *
from datetime import datetime, timezone
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

@bp.route("/create-dummy-data")
def create_dummy_data():    
    try:
        
        # Clear existing data if needed
        # db.session.query(SchedaUS).delete()
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
        loc5 = Localita(denom="Villa Romana", via="Via Appia Antica 15", citta="Roma", provincia="RM", cap="00179")
        loc6 = Localita(denom="Castello Medievale", via="Via Castello 3", citta="Firenze", provincia="FI", cap="50100")
        loc7 = Localita(denom="Necropoli Etrusca", via="Via degli Etruschi 8", citta="Tarquinia", provincia="VT", cap="01016")
        loc8 = Localita(denom="Museo Archeologico", via="Via Archeologia 12", citta="Bologna", provincia="BO", cap="40100")
        loc9 = Localita(denom="Teatro Greco", via="Via Teatro 9", citta="Siracusa", provincia="SR", cap="96100")
        loc10 = Localita(denom="Fortezza Antica", via="Via delle Mura 7", citta="Verona", provincia="VR", cap="37100")
        loc11 = Localita(denom="Antico Mercato", via="Piazza del Mercato 1", citta="Genova", provincia="GE", cap="16100")
        loc12 = Localita(denom="Tempio Romano", via="Via dei Templi 4", citta="Agrigento", provincia="AG", cap="92100")


        # Create dummy ente
        ente1 = Ente(nome="Soprintendenza Archeologia Roma", tel="0654321987", email="info@ente1.it", localita=loc1)
        ente2 = Ente(nome="Soprintendenza Archeologia Parma", tel="4589321987", email="info@ente2.it", localita=loc2)
        ente3 = Ente(nome="Museo Storico Nazionale", tel="0276543210", email="info@ente3.it", localita=loc3)
        ente4 = Ente(nome="Parco Archeologico Napoli", tel="0812345678", email="info@ente4.it", localita=loc4)
        ente5 = Ente(nome="Villa Romana Management", tel="0611122233", email="info@ente5.it", localita=loc5)
        ente6 = Ente(nome="Castello Fiorentino", tel="0559988776", email="info@ente6.it", localita=loc6)
        ente7 = Ente(nome="Soprintendenza Etrusca", tel="0766842301", email="info@ente7.it", localita=loc7)
        ente8 = Ente(nome="Teatro Greco Authority", tel="0931678902", email="info@ente8.it", localita=loc9)


        db.session.add_all([
            person1, person2, person3, person4, person5,
            loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8, loc9, loc10, loc11, loc12,
            ente1, ente2, ente3, ente4, ente5, ente6, ente7, ente8
        ])
        db.session.commit()

        dataset_max = 14

        # Create dummy dataset
        schede = []
        for i in range(1, dataset_max):
            scheda = SchedaUS(
                num_us=str(i*10),
                id_responsabile=person1.id,
                id_res_scientifico=person2.id,
                descrizione=f"Descrizione della scheda per l'unità stratigrafica",
                id_ente_resp=ente1.id,
                id_localita=loc1.id,
                data=datetime.now(timezone.utc),
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
                flottazione="si",
                setacciatura="a_campione",
                affidabilita_strat="Buona",
                modo_formazione="Deposizione antropica",
                elem_datanti="Ceramica",
                settore="Settore A",
                stato_conservazione="Buono",
                criteri_distinzione="Stratificazione",
                def_e_pos="Buca di palo",
            )
            schede.append(scheda)
        db.session.add_all(schede)

        reperti = []
        for i in range(1, dataset_max):
            for j in range(1, 3):
                reperto = RepertoNotevoleUS(
                    id_scheda_us=i,
                    numero_cassa = f"{i*10}{j*10}-RR",
                    sito = "PVG22MUR",
                    data = datetime.now(timezone.utc),
                    materiale = "Ceramica",
                    descrizione = "Vaso",
                    quantita = "1",
                    lavato = True if i % 2 == 0 else False,
                    siglato = False if i % 2 == 0 else True,
                    punto_stazione_totale = "Post",
                    coord_y = f'{i*10}',
                    coord_x = f'{i*10}',
                    coord_z = f'{i*10}',
                    note="Nessuna nota rilevante"
                )
                reperti.append(reperto)
        db.session.add_all(reperti)

        db.session.commit()

        flash(f"{len(schede)} schede create con successo", "success")
        return redirect(url_for("main.index"))
    except Exception as e:
        db.session.rollback()
        flash(f"Errore durante la creazione dei dati: {str(e)}", "error")
        return redirect(url_for("main.index"))