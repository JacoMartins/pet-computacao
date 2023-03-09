from db import db
from datetime import datetime

class ViagemModel(db.Model):
  __tablename__ = "viagens"

  id = db.Column(db.Integer, primary_key=True)
  id_linha = db.Column(db.Integer, db.ForeignKey("linhas.id"), nullable=False)
  id_sentido = db.Column(db.Integer, db.ForeignKey("sentidos.id"),nullable=False)
  data = db.Column(db.DateTime, nullable=False)
  origem = db.Column(db.String, nullable=False)
  destino = db.Column(db.String, nullable=False)
  horario_partida = db.Column(db.String, nullable=False)
  horario_chegada = db.Column(db.String, nullable=False)
  pago_inteira = db.Column(db.Integer, nullable=False, default=0)
  pago_meia = db.Column(db.Integer, nullable=False, default=0)
  gratuidade = db.Column(db.Integer, nullable=False, default=0)
  assentos_disponiveis = db.Column(db.Integer, nullable=False)
  criado_em = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
  atualizado_em = db.Column(db.DateTime, nullable=False)

  linha = db.relationship("LinhaModel", back_populates="viagens")
  sentido = db.relationship("SentidoModel", back_populates="viagens")
  reservas = db.relationship("ReservaModel", back_populates="viagem", cascade="all, delete")