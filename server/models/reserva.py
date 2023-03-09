from db import db
from datetime import datetime

class ReservaModel(db.Model):
  __tablename__ = "reservas"

  id = db.Column(db.Integer, primary_key=True)
  id_viagem = db.Column(db.Integer, db.ForeignKey("viagens.id"), nullable=False)
  id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
  assento = db.Column(db.Integer, nullable=False)
  forma_pagamento = db.Column(db.String(20), nullable=False)
  criado_em = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
  atualizado_em = db.Column(db.DateTime, nullable=True)

  viagem = db.relationship("ViagemModel", back_populates="reservas")
  usuario = db.relationship("UsuarioModel", back_populates="reservas")