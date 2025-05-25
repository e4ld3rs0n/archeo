from db import db
from sqlalchemy import event
from sqlalchemy.orm import Mapper



class Anagrafica(db.Model):
    __tablename__ = "anagrafica"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cognome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255), nullable=False)

    search_vector = db.Column(db.Text, index=True) ### Search vector

    schede_responsabile = db.relationship("SchedaUS", backref="responsabile", foreign_keys="SchedaUS.id_responsabile")
    schede_scientifico = db.relationship("SchedaUS", backref="responsabile_scientifico", foreign_keys="SchedaUS.id_res_scientifico")

    def __str__(self):
        return f"{self.nome} {self.cognome}"

    def update_search_vector(self):
        self.search_vector = " ".join([
            str(p) for p in [
                self.nome,
                self.cognome,
                self.email,
                self.tel
            ] if p
        ])

class Localita(db.Model):
    __tablename__ = "localita"

    id = db.Column(db.Integer, primary_key=True)
    denom = db.Column(db.String(255))
    via = db.Column(db.String(255), nullable=False)
    citta = db.Column(db.String(255), nullable=False)
    provincia = db.Column(db.String(255), nullable=False)
    cap = db.Column(db.String(6), nullable=False)

    search_vector = db.Column(db.Text, index=True) ### Search vector

    enti = db.relationship("Ente", backref="localita")
    schede = db.relationship("SchedaUS", backref="localita")

    def __str__(self):
        if self.denom:
            return f"{self.denom} {self.via} {self.citta}"
        else:
            return f"{self.via} {self.citta}"

    def update_search_vector(self):
        self.search_vector = " ".join([
            str(p) for p in [
                self.denom,
                self.via,
                self.citta,
                self.provincia,
                self.cap
            ] if p
        ])

class Ente(db.Model):
    __tablename__ = "ente"

    id = db.Column(db.Integer, primary_key=True)
    id_loc = db.Column(db.Integer, db.ForeignKey("localita.id"), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(255))
    email = db.Column(db.String(255))

    search_vector = db.Column(db.Text, index=True) ### Search vector

    scheda_responsabile = db.relationship("SchedaUS", backref="ente_responsabile", uselist=False, foreign_keys="SchedaUS.id_ente_resp")

    def __str__(self):
        return f"{self.nome} {self.localita.via} {self.localita.citta}"

    def update_search_vector(self):
        self.search_vector = " ".join([
            str(p) for p in [
                self.nome,
                self.tel,
                self.email,
                self.localita.via,
                self.localita.citta,
                self.localita.provincia,
                self.localita.cap
            ] if p
        ])

class SchedaUS(db.Model):
    __tablename__ = "scheda_us"

    id = db.Column(db.Integer, primary_key=True)
    num_us = db.Column(db.String(16), nullable=False, unique=True)
    id_responsabile = db.Column(db.Integer, db.ForeignKey("anagrafica.id"), nullable=False)
    id_res_scientifico = db.Column(db.Integer, db.ForeignKey("anagrafica.id"), nullable=False)
    descrizione = db.Column(db.String(2000), nullable=False)
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
    id_ortofoto = db.Column(db.Integer, db.ForeignKey("ortofoto.id"))

    search_vector = db.Column(db.Text, index=True) ### Search vector

    ortofoto = db.relationship("Ortofoto", backref="schede_us")
    foto = db.relationship("FotoUS", backref="foto_us", cascade="all, delete-orphan")
    seq_fisiche_a = db.relationship("SeqFisica", backref="scheda_a", foreign_keys="SeqFisica.id_seq_a")
    seq_fisiche_b = db.relationship("SeqFisica", backref="scheda_b", foreign_keys="SeqFisica.id_seq_b")
    seq_strat_a = db.relationship("SeqStrat", backref="scheda_strat_a", foreign_keys="SeqStrat.id_seq_a")
    seq_strat_b = db.relationship("SeqStrat", backref="scheda_strat_b", foreign_keys="SeqStrat.id_seq_b")
    reperti_notevoli = db.relationship("RepertoNotevoleUS", back_populates="scheda_us", foreign_keys="RepertoNotevoleUS.id_scheda_us", cascade="all, delete-orphan")

    def __str__(self):
        return f"US {self.num_us} {self.descrizione}"

    def update_search_vector(self):
        self.search_vector = " ".join([
            str(p) for p in [
                self.num_us,
                self.descrizione,
                self.colore,
                self.composizione,
                self.consistenza,
                self.interpretazione,
                self.note,
                self.elem_datanti,
                self.settore,
                self.stato_conservazione,
                self.data.strftime("%d/%m/%Y") if self.data else "",
                self.responsabile.nome if self.responsabile else "",
                self.responsabile.cognome if self.responsabile else "",
                self.responsabile_scientifico.nome if self.responsabile_scientifico else "",
                self.responsabile_scientifico.cognome if self.responsabile_scientifico else ""
            ] if p
        ])

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

    search_vector = db.Column(db.Text, index=True) ### Search vector

    scheda_us = db.relationship('SchedaUS', back_populates='reperti_notevoli', lazy=True)

    def __str__(self):
        return f"Reperto №{self.id} {self.descrizione}"

    def update_search_vector(self):
        self.search_vector = " ".join([
            str(p) for p in [
                self.numero_cassa,
                self.sito,
                self.data.strftime("%d/%m/%Y") if self.data else "",
                self.materiale,
                self.descrizione,
                "Lavato" if self.lavato else "",
                "Siglato" if self.siglato else "",
                self.quantita,
                self.punto_stazione_totale,
                self.note
            ] if p
        ])

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

class Ortofoto(db.Model):
    __tablename__ = "ortofoto"

    id = db.Column(db.Integer, primary_key=True)
    id_operatore = db.Column(db.Integer, db.ForeignKey("anagrafica.id"), nullable=False)
    descrizione = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    target = db.Column(db.String(255))
    note = db.Column(db.String(255))
    path_ortofoto = db.Column(db.String(255), nullable=False)
    completato = db.Column(db.Boolean, nullable=False)

    operatore = db.relationship("Anagrafica", backref="ortofoto")

class SacchettoMateriali(db.Model):
    __tablename__ = 'sac_mat'

    id = db.Column(db.Integer, primary_key=True)
    num_sac = db.Column(db.String(50), unique=True, nullable=False)      # N. sacchetto
    sito = db.Column(db.String(100), nullable=False)                     # Sito
    data = db.Column(db.Date, nullable=False)                            # Data
    id_us = db.Column(db.Integer, db.ForeignKey('scheda_us.id'), nullable=False)
    quadrato = db.Column(db.String(10))                                  # Quadrato
    materiale = db.Column(db.String(100), nullable=False)                # Materiale
    lavato = db.Column(db.Boolean, nullable=False, default=False)        # Lavato
    siglato = db.Column(db.Boolean, nullable=False, default=False)       # Siglato
    disegnato = db.Column(db.Boolean, nullable=False, default=False)     # Disegnato
    note = db.Column(db.Text)                                            # Note generali sul sacchetto

    search_vector = db.Column(db.Text, index=True)  ### Search vector

    # Relazioni
    scheda_us = db.relationship('SchedaUS', backref=db.backref('sac_mat', lazy='dynamic'), foreign_keys=[id_us])
    associazioni_casse = db.relationship('AssocSacCassa', back_populates='sacchetto', cascade='all, delete-orphan')

    def update_search_vector(self):
        self.search_vector = " ".join([
            str(p) for p in [
                self.num_sac,
                self.sito,
                self.data.strftime("%d/%m/%Y") if self.data else "",
                f"Quadrato {self.quadrato}",
                self.materiale,
                "Lavato" if self.lavato else "",
                "Siglato" if self.siglato else "",
                "Disegnato" if self.disegnato else "",
                self.note
            ] if p
        ])

    def __str__(self):
        return f"Sacchetto {self.num_sac}"


class CassaMateriali(db.Model):
    __tablename__ = 'cas_mat'

    id = db.Column(db.Integer, primary_key=True)
    num_cassa = db.Column(db.String(50), unique=True, nullable=False)   # N. cassa
    descrizione = db.Column(db.Text)                                    # Descrizione o ubicazione della cassa

    search_vector = db.Column(db.Text, index=True)  ### Search vector

    # Relazioni
    associazioni_sacchetti = db.relationship('AssocSacCassa', back_populates='cassa', cascade='all, delete-orphan')

    def update_search_vector(self):
        self.search_vector = " ".join([
            str(p) for p in [
                self.num_cassa,
                self.descrizione,
            ] if p
        ])

    def __str__(self):
        return f"Cassa {self.num_cassa}"


class AssocSacCassa(db.Model):
    __tablename__ = 'assoc_sac_cassa'

    id = db.Column(db.Integer, primary_key=True)
    id_sacchetto = db.Column(db.Integer, db.ForeignKey('sac_mat.id'), nullable=False)
    id_cassa = db.Column(db.Integer, db.ForeignKey('cas_mat.id'), nullable=False)
    quantita_totale = db.Column(db.Integer, nullable=False)          # Quantità totale per questa relazione
    quantita_diagnostica = db.Column(db.Integer)                    # Quantità diagnostica
    note_associazione = db.Column(db.Text)                          # Note specifiche alla relazione

    # Relazioni
    sacchetto = db.relationship('SacchettoMateriali', back_populates='associazioni_casse')
    cassa = db.relationship('CassaMateriali', back_populates='associazioni_sacchetti')
