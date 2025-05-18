from flask import Blueprint, redirect, url_for, flash
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import *

bp = Blueprint("delete", __name__)

@bp.route("/elimina/anagrafica/<int:id_anagrafica>", methods=["POST"])
def elimina_anagrafica(id_anagrafica):
    try:
        anagrafica = Anagrafica.query.get_or_404(id_anagrafica)
        
        nome = anagrafica.nome
        cognome = anagrafica.cognome
        
        db.session.delete(anagrafica)
        db.session.commit()
        flash(f"Anagrafica per {nome} {cognome} eliminata con successo.", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash(f"Errore {e.orig.pgcode}: impossibile eliminare questa anagrafica perché è ancora collegata ad altri record (ad esempio enti, località o altri riferimenti). Rimuovi prima i collegamenti.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Errore durante l'eliminazione dell'anagrafica: {str(e)}", "error")
    
    return redirect(url_for("view.visualizza_anagrafiche"))

@bp.route("/elimina/localita/<int:id_localita>", methods=["POST"])
def elimina_localita(id_localita):
    try:
        loc = Localita.query.get_or_404(id_localita)
        
        if loc.denom:
            desc = f"{loc.denom} {loc.via} {loc.citta}"
        else:
            desc = f"{loc.via} {loc.citta}" 
        
        db.session.delete(loc)
        db.session.commit()
        flash(f"Località {desc} eliminata con successo.", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash(f"Errore {e.orig.pgcode}: impossibile eliminare questa località perché è ancora collegata ad altri record (ad esempio enti). Rimuovi prima i collegamenti.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Errore durante l'eliminazione della località: {str(e)}", "error")
    
    return redirect(url_for("view.visualizza_localita"))

@bp.route("/elimina/ente/<int:id_ente>", methods=["POST"])
def elimina_ente(id_ente):
    try:
        ente = Ente.query.get_or_404(id_ente)
        
        desc = ente.nome 
        
        db.session.delete(ente)
        db.session.commit()
        flash(f"Ente {desc} eliminato con successo.", "success")
    except IntegrityError as e:
        db.session.rollback()
        flash(f"Errore {e.orig.pgcode}: impossibile eliminare questo ente perché è ancora collegato ad altri record (ad esempio schede US). Rimuovi prima i collegamenti.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Errore durante l'eliminazione dell'ente: {str(e)}", "error")
    
    return redirect(url_for("view.visualizza_enti"))