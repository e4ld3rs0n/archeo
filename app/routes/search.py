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

bp = Blueprint("search", __name__)

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')

    if query:
        anagrafiche = Anagrafica.query.filter(
            (Anagrafica.nome.ilike(f"%{query}%")) |
            (Anagrafica.cognome.ilike(f"%{query}%")) |
            (Anagrafica.email.ilike(f"%{query}%")) |
            (Anagrafica.tel.ilike(f"%{query}%"))
        ).all()

        localita = Localita.query.filter(
            (Localita.denom.ilike(f"%{query}%")) |
            (Localita.via.ilike(f"%{query}%")) |
            (Localita.citta.ilike(f"%{query}%")) |
            (Localita.provincia.ilike(f"%{query}%")) |
            (Localita.cap.ilike(f"%{query}%"))
        ).all()

        enti = Ente.query.filter(
            (Ente.nome.ilike(f"%{query}%")) |
            (Ente.tel.ilike(f"%{query}%")) |
            (Ente.email.ilike(f"%{query}%"))
        ).all()

        schede = SchedaUS.query.filter(
            (SchedaUS.num_us.ilike(f"%{query}%")) |
            (SchedaUS.descrizione.ilike(f"%{query}%")) |
            (SchedaUS.quadrato.ilike(f"%{query}%")) |
            (SchedaUS.settore.ilike(f"%{query}%")) |
            (SchedaUS.colore.ilike(f"%{query}%")) |
            (SchedaUS.composizione.ilike(f"%{query}%")) |
            (SchedaUS.consistenza.ilike(f"%{query}%")) |
            (SchedaUS.comp_organici.ilike(f"%{query}%")) |
            (SchedaUS.comp_inorganici.ilike(f"%{query}%")) |
            (SchedaUS.interpretazione.ilike(f"%{query}%")) |
            (SchedaUS.misure.ilike(f"%{query}%")) |
            (SchedaUS.note.ilike(f"%{query}%")) |
            (SchedaUS.flottazione.ilike(f"%{query}%")) |
            (SchedaUS.setacciatura.ilike(f"%{query}%")) |
            (SchedaUS.affidabilita_strat.ilike(f"%{query}%")) |
            (SchedaUS.modo_formazione.ilike(f"%{query}%")) |
            (SchedaUS.stato_conservazione.ilike(f"%{query}%")) |
            (SchedaUS.criteri_distinzione.ilike(f"%{query}%")) |
            (SchedaUS.def_e_pos.ilike(f"%{query}%")) |
            (SchedaUS.elem_datanti.ilike(f"%{query}%"))
        ).all()

        reperti = RepertoNotevoleUS.query.filter(
            (RepertoNotevoleUS.numero_cassa.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.sito.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.materiale.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.descrizione.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.quantita.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.punto_stazione_totale.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.coord_y.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.coord_x.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.coord_z.ilike(f"%{query}%")) |
            (RepertoNotevoleUS.note.ilike(f"%{query}%"))
        ).all()

        return render_template('view/risultati_ricerca.html', 
                               query=query, 
                               anagrafiche=anagrafiche, 
                               localita=localita, 
                               enti=enti, 
                               schede=schede,
                               reperti=reperti)
    return render_template('view/risultati_ricerca.html', query=None)