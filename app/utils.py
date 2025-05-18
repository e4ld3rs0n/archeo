from flask import Blueprint, render_template, redirect, url_for, flash, render_template_string
from sqlalchemy import *
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import *
import random
from faker import Faker

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    if not tables:
        # No tables exist — needs initialization
        flash("Attenzione: il database è vuoto. Prima di continuare è necessario inizializzarlo.", "info")
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
        try:
            db.session.query(RepertoNotevoleUS).delete()
            db.session.query(SchedaUS).delete()
            db.session.query(Ente).delete()
            db.session.query(Localita).delete()
            db.session.query(Anagrafica).delete()
        except Exception as e:
            db.session.rollback()
            flash(f"Errore durante l'eliminazione dei dati: {str(e)}", "error")
            return redirect(url_for("main.index"))

        db.session.commit()

        faker = Faker('it_IT')

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
        
        # Create dummy ente
        ente1 = Ente(nome="Soprintendenza Archeologia Roma", tel="0654321987", email="info@ente1.it", localita=loc1)
        ente2 = Ente(nome="Soprintendenza Archeologia Parma", tel="4589321987", email="info@ente2.it", localita=loc2)
        ente3 = Ente(nome="Museo Storico Nazionale", tel="0276543210", email="info@ente3.it", localita=loc3)
        ente4 = Ente(nome="Parco Archeologico Napoli", tel="0812345678", email="info@ente4.it", localita=loc4)
        ente5 = Ente(nome="Villa Romana Management", tel="0611122233", email="info@ente5.it", localita=loc5)
        ente6 = Ente(nome="Castello Fiorentino", tel="0559988776", email="info@ente6.it", localita=loc6)
        ente7 = Ente(nome="Soprintendenza Etrusca", tel="0766842301", email="info@ente7.it", localita=loc7)
        ente8 = Ente(nome="Teatro Greco Authority", tel="0931678902", email="info@ente8.it", localita=loc8)

        elements = [
            person1, person2, person3, person4, person5,
            loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8,
            ente1, ente2, ente3, ente4, ente5, ente6, ente7, ente8
        ]

        db.session.add_all(elements)
        db.session.commit()

        dataset_max = 16

        composizioni = ["Terra", "Sabbia", "Argilla", "Ghiaia"]
        colori = ["Marrone", "Grigio", "Nero", "Rosso", "Giallo"]
        consistenze = ["Soffice", "Media", "Dura"]
        org = ["Carboni", "Semi", "Legno"]
        inorg = ["Mattoni", "Ceramica", "Pietre"]
        interpretazioni = ["Strato abitativo", "Rinterro", "Uso agricolo", "Struttura"]
        modi_formazione = ["Deposizione antropica", "Deposizione naturale", "Disturbo moderno"]
        elem = ["Ceramica", "Metallo", "Ossa", "Carboni"]

        # Create dummy dataset
        schede = []
        for i in range(1, dataset_max):
            scheda = SchedaUS(
                num_us=str(random.randint(100, 900)),
                responsabile=random.choice([person1, person2, person3, person4, person5]),
                responsabile_scientifico=random.choice([person1, person2, person3, person4, person5]),
                descrizione=faker.sentence(nb_words=6),
                id_ente_resp=random.choice([ente1.id, ente2.id, ente3.id, ente4.id, ente5.id, ente6.id, ente7.id, ente8.id]),
                id_localita=random.choice([loc1.id, loc2.id, loc3.id, loc4.id, loc5.id, loc6.id, loc7.id, loc8.id]),
                data=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 365)),
                quadrato=f"{random.choice(['A', 'B', 'C', 'C'])}{random.randint(1,10)}",
                colore=random.choice(colori),
                composizione=random.choice(composizioni),
                consistenza=random.choice(consistenze),
                comp_organici=random.choice(org),
                comp_inorganici=random.choice(inorg),
                interpretazione=random.choice(interpretazioni),
                misure=random.choice(["1x1m", "1.5x1.5m", "2x2m"]),
                note=faker.text(max_nb_chars=100),
                campionature=random.choice([True, False]),
                flottazione=random.choice(["si", "no", "a_campione", "integrale"]),
                setacciatura=random.choice(["si", "no", "a_campione", "integrale"]),
                affidabilita_strat=random.choice(["Buona", "Media", "Scarsa"]),
                modo_formazione=random.choice(modi_formazione),
                elem_datanti=random.choice(elem),
                settore=random.choice(["Settore A", "Settore B", "Settore C"]),
                stato_conservazione=random.choice(["Buono", "Discreto", "Pessimo"]),
                criteri_distinzione="Stratificazione",
                def_e_pos=random.choice(["Buca di palo", "Struttura muraria", "Fossa", "Taglio"]),
            )
            schede.append(scheda)

        db.session.add_all(schede)
        db.session.flush()

        reperti = []
        for i in range(1, dataset_max):
            for j in range(1, 3):
                reperto = RepertoNotevoleUS(
                    id_scheda_us=random.choice(schede).id,
                    numero_cassa = f"{i*10}{j*10}-RR",
                    sito = random.choice(["PVG22-MUR", "PVG24-MUR", "PVG20-MUR"]),
                    data = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 365)),
                    materiale = random.choice(["Ceramica", "Terracotta", "Metallo", "Ossa", "Vetro"]),
                    descrizione = random.choice(["Vaso", "Piatto", "Anfora", "Coppa", "Ciotola"]),
                    quantita = random.choice(["1", "2", "3", "4", "5"]),
                    lavato = True if i % 2 == 0 else False,
                    siglato = False if i % 2 == 0 else True,
                    punto_stazione_totale = "Post",
                    coord_y = f'{random.uniform(-10.0, 10.0)}',
                    coord_x = f'{random.uniform(-10.0, 10.0)}',
                    coord_z = f'{random.uniform(-10.0, 10.0)}',
                    note=faker.text(max_nb_chars=100)
                )
                reperti.append(reperto)
        
        db.session.add_all(reperti)

        db.session.flush()
        # Forza aggiornamento degli indici di ricerca
        for scheda in schede:
            scheda.update_search_vector()
        
        for e in elements:
            e.update_search_vector()

        for r in reperti:
            r.update_search_vector()

        db.session.commit()

        flash(f"{len(schede)} schede create con successo", "success")
        return redirect(url_for("main.index"))
    except Exception as e:
        db.session.rollback()
        flash(f"Errore durante la creazione dei dati: {str(e)}", "error")
        return redirect(url_for("main.index"))