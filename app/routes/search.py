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
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import *

bp = Blueprint("search", __name__)

@bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("view/risultati_ricerca.html", query=None, results=[])
    
    results = []

    def build_results(model, label, url_func):
        search_col = model.search_vector
        relevance = func.length(search_col) - func.length(func.replace(search_col, query, ""))
        matches = model.query.filter(search_col.ilike(f"%{query}%")) \
                             .add_columns(relevance.label("relevance")) \
                             .order_by(relevance.desc()) \
                             .all()
        
        for obj, relevance_score in matches:
            results.append({
                "tipo": label,
                "titolo": getattr(obj, "descrizione", None) or getattr(obj, "nome", None) or "Risultato",
                "url": url_func(obj),
                "snippet": build_snippet(obj.search_vector, query),
                "score": relevance_score
            })

    def build_snippet(text, keyword):
        import re
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        snippet = pattern.sub(r"<mark>\g<0></mark>", text)
        return snippet if len(snippet) < 300 else snippet[:297] + "..."
    
    build_results(SchedaUS, "Scheda US", lambda o: url_for("view.scheda", id=o.id))
    build_results(RepertoNotevoleUS, "Reperto", lambda o: url_for("view.reperto_notevole", id=o.id))
    build_results(Anagrafica, "Anagrafica", lambda o: url_for("view.visualizza_anagrafiche"))
    build_results(Localita, "Località", lambda o: url_for("view.visualizza_localita"))
    build_results(Ente, "Ente", lambda o: url_for("view.visualizza_enti"))

    results.sort(key=lambda r: r["score"], reverse=True)

    return render_template("view/risultati_ricerca.html", query=query, results=results)
