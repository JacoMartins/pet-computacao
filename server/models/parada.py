from db import db
from datetime import datetime

class ParadaModel(db.Model):
    __tablename__ = "paradas"

    id = db.Column(db.Integer, primary_key=True)
    id_linha = db.Column(db.Integer, db.ForeignKey("linhas.id"), nullable=False)
    id_sentido = db.Column(db.Integer, db.ForeignKey("sentidos.id"), nullable=False)
    parada = db.Column(db.String, nullable=False)
    minutos = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow())
    atualizado_em = db.Column(db.DateTime, nullable=True)

    linha = db.relationship("LinhaModel", back_populates="paradas", uselist='false')
    sentido = db.relationship("SentidoModel", back_populates="paradas", uselist='false')