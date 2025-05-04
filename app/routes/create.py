from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for, flash, render_template_string
from sqlalchemy import *
from datetime import datetime
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