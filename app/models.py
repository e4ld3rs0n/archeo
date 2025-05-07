from db import db

class Anagrafica(db.Model):
    __tablename__ = "anagrafica"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cognome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255), nullable=False)

    schede_responsabile = db.relationship("ModSchedaUs", backref="responsabile", foreign_keys="ModSchedaUs.id_responsabile")
    schede_scientifico = db.relationship("ModSchedaUs", backref="responsabile_scientifico", foreign_keys="ModSchedaUs.id_res_scientifico")


class Localita(db.Model):
    __tablename__ = "localita"

    id = db.Column(db.Integer, primary_key=True)
    denom = db.Column(db.String(255))
    via = db.Column(db.String(255), nullable=False)
    citta = db.Column(db.String(255), nullable=False)
    provincia = db.Column(db.String(255), nullable=False)
    cap = db.Column(db.String(6), nullable=False)

    enti = db.relationship("Ente", backref="localita")
    schede = db.relationship("ModSchedaUs", backref="localita")


class Ente(db.Model):
    __tablename__ = "ente"

    id = db.Column(db.Integer, primary_key=True)
    id_loc = db.Column(db.Integer, db.ForeignKey("localita.id"), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255))
    email = db.Column(db.String(255))

    scheda_responsabile = db.relationship("ModSchedaUs", backref="ente_responsabile", uselist=False, foreign_keys="ModSchedaUs.id_ente_resp")


class ModSchedaUs(db.Model):
    __tablename__ = "mod_scheda_us"

    id = db.Column(db.Integer, primary_key=True)
    num_us = db.Column(db.String(16), nullable=False, unique=True)
    id_responsabile = db.Column(db.Integer, db.ForeignKey("anagrafica.id"), nullable=False)
    id_res_scientifico = db.Column(db.Integer, db.ForeignKey("anagrafica.id"), nullable=False)
    descrizione = db.Column(db.String(255), nullable=False)
    id_ente_resp = db.Column(db.Integer, db.ForeignKey("ente.id"), nullable=False)
    id_localita = db.Column(db.Integer, db.ForeignKey("localita.id"), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    quadrato = db.Column(db.String(255), nullable=False)
    colore = db.Column(db.String(255), nullable=False)
    composizione = db.Column(db.String(255), nullable=False)
    consistenza = db.Column(db.String(255), nullable=False)
    comp_organici = db.Column(db.String(255))
    comp_inorganici = db.Column(db.String(255))
    interpretazione = db.Column(db.String(255), nullable=False)
    misure = db.Column(db.String(255), nullable=False)
    note = db.Column(db.String(255), nullable=True)
    campionature = db.Column(db.Boolean, nullable=False)
    flottazione = db.Column(db.Boolean, nullable=False)
    setacciatura = db.Column(db.String(255))
    affidabilita_strat = db.Column(db.String(255))
    modo_formazione = db.Column(db.String(255))
    elem_datanti = db.Column(db.String(255))

    piante = db.relationship("PiantaUS", backref="pianta_us", cascade="all, delete-orphan")
    foto = db.relationship("FotoUS", backref="foto_us", cascade="all, delete-orphan")
    ortofoto = db.relationship("OrtofotoUS", backref="ortofoto_us", cascade="all, delete-orphan")
    seq_fisiche_a = db.relationship("SeqFisica", backref="scheda_a", foreign_keys="SeqFisica.id_seq_a")
    seq_fisiche_b = db.relationship("SeqFisica", backref="scheda_b", foreign_keys="SeqFisica.id_seq_b")
    seq_strat_a = db.relationship("SeqStrat", backref="scheda_strat_a", foreign_keys="SeqStrat.id_seq_a")
    seq_strat_b = db.relationship("SeqStrat", backref="scheda_strat_b", foreign_keys="SeqStrat.id_seq_b")

class PiantaUS(db.Model):
    __tablename__ = "pianta_us"

    id = db.Column(db.Integer, primary_key=True)
    id_mod_scheda_us = db.Column(db.Integer, db.ForeignKey("mod_scheda_us.id"), nullable=False)
    path_pianta = db.Column(db.String(255), nullable=False)

class FotoUS(db.Model):
    __tablename__ = "foto_us"

    id = db.Column(db.Integer, primary_key=True)
    id_mod_scheda_us = db.Column(db.Integer, db.ForeignKey("mod_scheda_us.id"), nullable=False)
    path_foto = db.Column(db.String(255), nullable=False)

class OrtofotoUS(db.Model):
    __tablename__ = "ortifoto_us"

    id = db.Column(db.Integer, primary_key=True)
    id_mod_scheda_us = db.Column(db.Integer, db.ForeignKey("mod_scheda_us.id"), nullable=False)
    path_ortofoto = db.Column(db.String(255), nullable=False)

class SeqFisica(db.Model):
    __tablename__ = "seq_fisica"

    id = db.Column(db.Integer, primary_key=True)
    id_seq_a = db.Column(db.Integer, db.ForeignKey("mod_scheda_us.id"), nullable=False)
    id_seq_b = db.Column(db.Integer, db.ForeignKey("mod_scheda_us.id"), nullable=False)
    sequenza = db.Column(db.String(255), nullable=False)


class SeqStrat(db.Model):
    __tablename__ = "seq_strat"

    id = db.Column(db.Integer, primary_key=True)
    id_seq_a = db.Column(db.Integer, db.ForeignKey("mod_scheda_us.id"), nullable=False)
    id_seq_b = db.Column(db.Integer, db.ForeignKey("mod_scheda_us.id"), nullable=False)
