from flask import request as req
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from db import db
from models import ViagemModel
from schemas import ViagemSchema, PlainViagemSchema


blp = Blueprint("Viagens", __name__, description="Operações com viagens.")


@blp.route('/viagens')
class ViagemList(MethodView):
  @blp.response(200, ViagemSchema(many=True))
  def get(self):
    viagens = ViagemModel.query.all()

    return viagens
  

@blp.route('/viagem')
class Viagem(MethodView):
  @blp.response(200, ViagemSchema)
  def get(self):
    viagem_id = req.args.get('id')
    viagem = ViagemModel.query.get_or_404(viagem_id)

    return viagem
  
  @blp.arguments(ViagemSchema)
  @blp.response(201, ViagemSchema)
  def post(self, viagem_data):
    viagem = ViagemModel(**viagem_data)

    try:
      db.session.add(viagem)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, "An error ocurred while inserting item to table 'viagem'.")

    return viagem
  
  @blp.arguments(ViagemSchema)
  @blp.response(200, ViagemSchema)
  def put(self, viagem_data):
    viagem_id = req.args.get('id')
    viagem = ViagemModel.query.get(viagem_id)

    if viagem:
      viagem.id_linha = viagem_data["id_linha"]
      viagem.id_sentido = viagem_data["id_sentido"]
      viagem.data = viagem_data["data"]
      viagem.origem = viagem_data["origem"]
      viagem.destino = viagem_data["destino"]
      viagem.horario_partida = viagem_data["horario_partida"]
      viagem.horario_chegada = viagem_data["horario_chegada"]
      viagem.pago_inteira = viagem_data["pago_inteira"]
      viagem.pago_meia = viagem_data["pago_meia"]
      viagem.gratuidade = viagem_data["gratuidade"]
      viagem.assentos_disponiveis = viagem_data["assentos_disponiveis"]
      viagem.atualizado_em = datetime.now().isoformat()
    else:
      viagem = ViagemModel(id=viagem_id, **viagem_data)

    try:
      db.session.add(viagem)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, "An error ocurred while inserting item to table 'viagem'.")

    return viagem
  
  @blp.response(204)
  def delete(self):
    viagem_id = req.args.get('id')
    viagem = ViagemModel.query.get(viagem_id)

    if viagem:
      db.session.delete(viagem)
      db.session.commit()
    else:
      abort(404, "Item not found.")

    return {"message": "Viagem excluida."}