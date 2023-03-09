from flask import request as req
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from db import db
from models import ReservaModel
from schemas import ReservaSchema, PlainReservaSchema


blp = Blueprint("Reservas", __name__, description="Operações com reservas.")


@blp.route('/reservas')
class ReservaList(MethodView):
  @blp.response(200, ReservaSchema(many=True))
  def get(self):
    reservas = ReservaModel.query.all()

    return reservas
  

@blp.route('/reserva')
class Reserva(MethodView):
  @blp.response(200, ReservaSchema)
  def get(self):
    reserva_id = req.args.get('id')
    reserva = ReservaModel.query.get_or_404(reserva_id)

    return reserva
  
  @jwt_required()
  @blp.arguments(ReservaSchema)
  @blp.response(201, ReservaSchema)
  def post(self, reserva_data):
    reserva = ReservaModel(**reserva_data)

    try:
      db.session.add(reserva)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, "An error ocurred while inserting item to table 'reserva'.")

    return reserva
  
  @jwt_required()
  @blp.arguments(ReservaSchema)
  @blp.response(200, ReservaSchema)
  def put(self, reserva_data):
    reserva_id = req.args.get('id')
    reserva = ReservaModel.query.get(reserva_id)

    if reserva:
      reserva.id_viagem = reserva_data["id_viagem"]
      reserva.id_usuario = reserva_data["id_usuario"]
      reserva.assento = reserva_data["assento"]
      reserva.forma_pagamento = reserva_data["forma_pagamento"]
      reserva.atualizado_em = datetime.now().isoformat()
    else:
      reserva = ReservaModel(id=reserva_id, **reserva_data)

    try:
      db.session.add(reserva)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, "An error ocurred while updating item from table 'reserva'.")

    return reserva

  @jwt_required()
  @blp.response(204)
  def delete(self):
    reserva_id = req.args.get('id')
    reserva = ReservaModel.query.get(reserva_id)

    if reserva:
      try:
        db.session.delete(reserva)
        db.session.commit()
      except SQLAlchemyError:
        abort(500, "An error ocurred while deleting item from table 'reserva'.")
    else:
      abort(404, "Item not found.")

    return {"message": "Reserva excluida."}