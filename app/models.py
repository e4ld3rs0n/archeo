from db import db

class Anagrafica(db.Model):
    __tablename__ = "anagrafica"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cognome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255), nullable=False)

    schede_responsabile = db.relationship("SchedaUS", backref="responsabile", foreign_keys="SchedaUS.id_responsabile")
    schede_scientifico = db.relationship("SchedaUS", backref="responsabile_scientifico", foreign_keys="SchedaUS.id_res_scientifico")

class Localita(db.Model):
    __tablename__ = "localita"

    id = db.Column(db.Integer, primary_key=True)
    denom = db.Column(db.String(255))
    via = db.Column(db.String(255), nullable=False)
    citta = db.Column(db.String(255), nullable=False)
    provincia = db.Column(db.String(255), nullable=False)
    cap = db.Column(db.String(6), nullable=False)

    enti = db.relationship("Ente", backref="localita")
    schede = db.relationship("SchedaUS", backref="localita")

class Ente(db.Model):
    __tablename__ = "ente"

    id = db.Column(db.Integer, primary_key=True)
    id_loc = db.Column(db.Integer, db.ForeignKey("localita.id"), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255))
    email = db.Column(db.String(255))

    scheda_responsabile = db.relationship("SchedaUS", backref="ente_responsabile", uselist=False, foreign_keys="SchedaUS.id_ente_resp")

class SchedaUS(db.Model):
    __tablename__ = "scheda_us"

    id = db.Column(db.Integer, primary_key=True)
    num_us = db.Column(db.String(16), nullable=False, unique=True)
    id_responsabile = db.Column(db.Integer, db.ForeignKey("anagrafica.id"), nullable=False)
    id_res_scientifico = db.Column(db.Integer, db.ForeignKey("anagrafica.id"), nullable=False)
    descrizione = db.Column(db.String(255), nullable=False)
    id_ente_resp = db.Column(db.Integer, db.ForeignKey("ente.id"), nullable=False)
    id_localita = db.Column(db.Integer, db.ForeignKey("localita.id"), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    quadrato = db.Column(db.String(255), nullable=False)
    settore = db.Column(db.String(128))                             ### Nuovo, Settore
    colore = db.Column(db.String(255))
    composizione = db.Column(db.String(255))
    consistenza = db.Column(db.String(255), nullable=False)
    comp_organici = db.Column(db.String(255))
    comp_inorganici = db.Column(db.String(255))
    interpretazione = db.Column(db.String(255))
    misure = db.Column(db.String(255))
    note = db.Column(db.String(2000), nullable=True)
    campionature = db.Column(db.Boolean, nullable=False)
    flottazione = db.Column(db.String(16), nullable=False)          ### Non è più un booleano
    setacciatura = db.Column(db.String(16), nullable=False)         ### Non è più un booleano
    affidabilita_strat = db.Column(db.String(255))
    modo_formazione = db.Column(db.String(255))
    stato_conservazione = db.Column(db.String(255))                 ### Nuovo, Stato di conservazione
    criteri_distinzione = db.Column(db.String(255), nullable=False) ### Nuovo, Criteri di distinzione
    def_e_pos = db.Column(db.String(255))                           ### Nuovo, definizione e posizione
    elem_datanti = db.Column(db.String(255))

    pianta_filename = db.Column(db.String(255))
    ortofoto_filename = db.Column(db.String(255))

    foto = db.relationship("FotoUS", backref="foto_us", cascade="all, delete-orphan")
    seq_fisiche_a = db.relationship("SeqFisica", backref="scheda_a", foreign_keys="SeqFisica.id_seq_a")
    seq_fisiche_b = db.relationship("SeqFisica", backref="scheda_b", foreign_keys="SeqFisica.id_seq_b")
    seq_strat_a = db.relationship("SeqStrat", backref="scheda_strat_a", foreign_keys="SeqStrat.id_seq_a")
    seq_strat_b = db.relationship("SeqStrat", backref="scheda_strat_b", foreign_keys="SeqStrat.id_seq_b")
    reperti_notevoli = db.relationship("RepertoNotevoleUS", back_populates="scheda_us", foreign_keys="RepertoNotevoleUS.id_scheda_us", cascade="all, delete-orphan")

class FotoUS(db.Model):
    __tablename__ = "foto_us"

    id = db.Column(db.Integer, primary_key=True)
    id_scheda_us = db.Column(db.Integer, db.ForeignKey("scheda_us.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)

class RepertoNotevoleUS(db.Model):
    __tablename__ = "reperto_notevole_us"

    id = db.Column(db.Integer, primary_key=True)
    id_scheda_us = db.Column(db.Integer, db.ForeignKey("scheda_us.id"), nullable=False)
    numero_cassa = db.Column(db.String(255), nullable=False)
    sito = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    materiale = db.Column(db.String(255), nullable=False)
    descrizione = db.Column(db.String(255), nullable=False)
    quantita = db.Column(db.String(255))
    lavato = db.Column(db.Boolean, nullable=False)
    siglato = db.Column(db.Boolean, nullable=False)
    punto_stazione_totale = db.Column(db.String(255))
    coord_y = db.Column(db.String(255))
    coord_x = db.Column(db.String(255))
    coord_z = db.Column(db.String(255))
    note = db.Column(db.String(2000), nullable=True)

    scheda_us = db.relationship('SchedaUS', back_populates='reperti_notevoli', lazy=True)

class SeqFisica(db.Model):
    __tablename__ = "seq_fisica"

    id = db.Column(db.Integer, primary_key=True)
    id_seq_a = db.Column(db.Integer, db.ForeignKey("scheda_us.id"), nullable=False)
    id_seq_b = db.Column(db.Integer, db.ForeignKey("scheda_us.id"), nullable=False)
    sequenza = db.Column(db.String(255), nullable=False)

class SeqStrat(db.Model):
    __tablename__ = "seq_strat"

    id = db.Column(db.Integer, primary_key=True)
    id_seq_a = db.Column(db.Integer, db.ForeignKey("scheda_us.id"), nullable=False)
    id_seq_b = db.Column(db.Integer, db.ForeignKey("scheda_us.id"), nullable=False)
