import os
from flask import (
    Blueprint, 
    render_template, 
    flash, 
    redirect, 
    url_for, 
    send_from_directory,
    Response,
    session,
    current_app as app
)
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from models import *
from graphviz import Digraph

bp = Blueprint("view", __name__)

def build_table_for_reperti(record):
    headers = [
        "ID", "US", "Numero cassa", "Sito", "Data",
        "Materiale", "Descrizione", "Quantità", "Lavato", "Siglato",
        "Punto stazione totale", "Coordinate", "Note"
    ]
    rows = []
    for r in record:
        rows.append([
            f'<a href="{url_for("view.reperto_notevole", id=r.id)}">Reperto №{r.id}</a>',
            f'<a href="{url_for("view.scheda", id=r.scheda_us.id)}">US {r.scheda_us.num_us}</a>',
            r.numero_cassa,
            r.sito,
            r.data.strftime('%d/%m/%Y') if r.data else '',
            r.materiale,
            r.descrizione,
            r.quantita,
            "&#10004;" if r.lavato else "",
            "&#10004;" if r.siglato else "",
            r.punto_stazione_totale,
            f"{r.coord_x}, {r.coord_y}, {r.coord_z}" if r.coord_x and r.coord_y and r.coord_z else "Non presenti",
            r.note or "",
        ])
    return headers, rows

def build_table_for_schede(record):
    labels = {
        "si": "Sì",
        "no": "No",
        "integrale": "Integrale",
        "a_campione": "A campione"
    }
    
    headers = [
        "US", "Descrizione", "Località", "Ente responsabile", "Data", "Quadrato", "Settore", "Colore",
        "Composizione", "Consistenza", "Componenti organici", "Componenti inorganici", "Campionature", 
        "Flottazione", "Setacciatura", "Interpretazione", "Misure", "Note" 
    ]
        
    rows = []
    for r in record:
        rows.append([
            f'<a href="{url_for("view.scheda", id=r.id)}">US {r.num_us}</a>',
            r.descrizione,
            f"{r.localita.via} - {r.localita.citta}" if r.localita else "",
            r.ente_responsabile.nome if r.ente_responsabile else "",
            r.data.strftime('%d/%m/%Y') if r.data else '',
            r.quadrato,
            r.settore,
            r.colore,
            r.composizione,
            r.consistenza,
            r.comp_organici,
            r.comp_inorganici,
            "Sì" if r.campionature == True else "No",
            labels.get(r.flottazione, r.flottazione),
            labels.get(r.setacciatura, r.setacciatura),
            r.interpretazione,
            r.misure,
            r.note or ""
        ])
    return headers, rows

def build_table_for_ortofoto(record):
    headers = [
        "Descrizione", "Link", "US associate", "Data", "Operatore", "Completato", "Target", "Note"
    ]
        
    rows = []
    for r in record:        
        schede_us = r.schede_us
        us_list = ", ".join([f"<a href=\"{url_for('view.scheda', id=s.id)}\">US {s.num_us}</a>" for s in schede_us]) if schede_us else "N/D"

        operatore = Anagrafica.query.get(r.id_operatore)
        name_and_surname = f"{operatore.nome} {operatore.cognome}" if operatore else "N/A"

        rows.append([
            r.descrizione,
            f'<a href="{r.path_ortofoto}">Apri link</a>',
            us_list,
            r.data.strftime('%d/%m/%Y') if r.data else '',
            name_and_surname,
            "&#10004;" if r.completato else "",
            r.target,
            r.note
        ])
    return headers, rows

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
    view = session.get("default_view", "card")
    
    if view == "card":
        records = SchedaUS.query.order_by(SchedaUS.num_us.asc()).all()
        return render_template(
            "view/visualizza_schede.html", 
            records=records, 
            title=page_title)
    elif view == "grid":
        headers, rows = build_table_for_schede(SchedaUS.query.order_by(SchedaUS.num_us.asc()).all())
        return render_template(
            "view/visualizza_schede.html", 
            headers=headers,
            rows=rows, 
            title=page_title)

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
    headers, rows = build_table_for_reperti(reperti_notevoli)
    
    return render_template(
        "view/visualizza_reperti_notevoli.html", 
        headers=headers,
        rows=rows, 
        title=page_title
        )

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
    
    headers, rows = build_table_for_ortofoto(ortofoto)

    return render_template(
        "view/visualizza_ortofoto.html", 
        headers=headers,
        rows=rows, 
        title=page_title)

@bp.route("/genera_grafo_stratigrafico", methods=["GET"])
def genera_grafo():
    # 1) crea il Digraph top-down
    dot = Digraph('Stratigrafia', format='svg', engine='dot')
    dot.graph_attr.update({
        'rankdir': 'TB',
        'splines': 'true',
        'overlap': 'false',
        'bgcolor': 'transparent',
    })
    dot.node_attr.update({
        'shape': 'box',
        'style': 'filled,rounded',
        'fillcolor': '#f9f9f9',
        'color': '#666666',
        'fontname': 'Helvetica',
        'fontsize': '12',
    })
    dot.edge_attr.update({
        'color': '#666666',
        'arrowsize': '0.8',
        'penwidth': '1',
        'fontname': 'Helvetica',
        'fontsize': '9',
    })

    # 2) relazioni e ID coinvolti
    rels = SeqStrat.query.all()
    coinvolti = {r.id_seq_a for r in rels} | {r.id_seq_b for r in rels}

    # 3) carica solo le SchedaUS coinvolte
    schede = SchedaUS.query.filter(SchedaUS.id.in_(list(coinvolti))).all()
    info_map = {s.id: (s.num_us, s.descrizione or "") for s in schede}

    # 4) nodi con link e tooltip
    for id_us in sorted(coinvolti):
        num, desc = info_map[id_us]
        href = url_for('view.scheda', id=id_us)
        label = f"US {num}"
        dot.node(
            str(id_us),
            label=label,
            href=href,
            tooltip=desc,
            target="_self"   # o "_blank" per aprire in nuova scheda
        )

    # 5) archi
    for r in rels:
        if r.id_seq_a in info_map and r.id_seq_b in info_map:
            dot.edge(
                str(r.id_seq_a),
                str(r.id_seq_b)
            )

    # 6) esporta SVG
    svg = dot.pipe().decode('utf-8')
    return Response(svg, mimetype='image/svg+xml')

@bp.route("/grafo_stratigrafico", methods=["GET"])
def visualizza_grafo():
    page_title = "Grafo stratigrafico"

    rels = SeqStrat.query.all()
    if not rels:
        return render_template(
            "view/grafo_stratigrafico.html", 
            title=page_title,
            grafo_svg=None
        )

    svg = genera_grafo().get_data(as_text=True)
    return render_template(
        "view/grafo_stratigrafico.html", 
        title=page_title,
        grafo_svg=svg
        )