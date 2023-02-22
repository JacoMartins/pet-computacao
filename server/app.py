from flask import Flask, request as req, jsonify, make_response as res
from flask_cors import CORS, cross_origin
from datetime import datetime

from database.db import simple

simple.setup()

today = datetime.now()

iso_date = today.isoformat()

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def index():
  return "Bem-vindo ao sistema de reservas de linha de ônibus do Câmpus UFC."

# Linhas

@app.route("/linha", methods=['GET'])
def get_linha():
  if req.args.get('cod'):
    result = simple.linha.get_one(where={
      'field': 'cod',
      'operator': '=',
      'value': req.args.get('cod')
    })

    return res(jsonify(result), result['status'])
    
  result = simple.linha.get_all()

  return res(jsonify(result), result['status'])


@app.route("/linha", methods=['POST'])
def post_linha():
  data = req.get_json()
  data['criado_em'] = iso_date
  data['atualizado_em'] = iso_date

  result = simple.linha.insert(**data)

  return res(jsonify(result), result['status'])

@app.route("/linha", methods=['PUT'])
def put_linha():
  id = req.args.get('id')
  data = req.get_json()

  data['criado_em'] = simple.linha.get_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })['data']['criado_em']

  data['atualizado_em'] = iso_date

  result = simple.linha.update_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  }, data=data)

  return res(jsonify(result), result['status'])

@app.route("/linha", methods=['DELETE'])
def delete_linha():
  id = req.args.get('id')

  result = simple.linha.delete_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })

  return res(jsonify(result), result['status'])

# Viagens

@app.route('/viagem', methods=['GET'])
def get_viagem():
  if req.args.get('id'):
    result = simple.viagem.get_one(where={
      'field': 'id',
      'operator': '=',
      'value': req.args.get('id')
    })

    return res(jsonify(result), result['status'])

  elif req.args.get('id_linha'):
    result = simple.viagem.get_one(where={
      'field': 'id_linha',
      'operator': '=',
      'value': req.args.get('id_linha')
    })

    return res(jsonify(result), result['status'])

  elif req.args.get('id_sentido'):
    result = simple.viagem.get_one(where={
      'field': 'id_sentido',
      'operator': '=',
      'value': req.args.get('id_sentido')
    })

    return res(jsonify(result), result['status'])
    
  result = simple.viagem.get_all()

  return res(jsonify(result), result['status'])

@app.route("/viagem", methods=['POST'])
def post_viagem():
  data = req.get_json()
  data['criado_em'] = iso_date
  data['atualizado_em'] = iso_date

  result = simple.viagem.insert(**data)

  return res(jsonify(result), result['status'])

@app.route("/viagem", methods=['PUT'])
def put_viagem():
  id = req.args.get('id')
  data = req.get_json()

  data['criado_em'] = simple.viagem.get_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })['data']['criado_em']

  data['atualizado_em'] = iso_date

  result = simple.viagem.update_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  }, data=data)

  return res(jsonify(result), result['status'])

@app.route("/viagem", methods=['DELETE'])
def delete_viagem():
  id = req.args.get('id')

  result = simple.viagem.delete_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })

  return res(jsonify(result), result['status'])

# Paradas

@app.route('/parada', methods=['GET'])
def get_parada():
  if req.args.get('id'):
    result = db_parada.get(req.args.get('id'))
    return res(jsonify(result), result['status'])
  if req.args.get('linha'):
    result = db_parada.get_where('id_linha', '=', req.args.get('linha'))
    return res(jsonify(result), result['status'])

  result = db_parada.get_all()
  return res(jsonify(result), result['status'])

@app.route("/parada", methods=['POST'])
def post_parada():
  data = req.get_json()

  result = db_parada.insert(data)

  return res(jsonify(result), result['status'])

@app.route("/parada", methods=['PUT'])
def put_parada():
  id = req.args.get('id')
  data = req.get_json()

  result = db_parada.update(id, data)

  return res(jsonify(result), result['status'])

@app.route("/parada", methods=['DELETE'])
def delete_parada():
  id = req.args.get('id')

  result = db_parada.delete(id)

  return res(jsonify(result), result['status'])

@app.route('/reserva', methods=['GET'])
def get_reserva():
  if req.args.get('id'):
    result = db_reserva.get(req.args.get('id'))
    return res(jsonify(result), result['status'])
  if req.args.get('viagem'):
    result = db_reserva.get_where('id_viagem', '=', req.args.get('viagem'))
    return res(jsonify(result), result['status'])

  result = db_reserva.get_all()
  return res(jsonify(result), result['status'])

@app.route("/reserva", methods=['POST'])
def post_reserva():
  data = req.get_json()

  result = db_reserva.insert(data)

  return res(jsonify(result), result['status'])

@app.route("/reserva", methods=['PUT'])
def put_reserva():
  id = req.args.get('id')
  data = req.get_json()

  result = db_reserva.update(id, data)

  return res(jsonify(result), result['status'])

@app.route("/reserva", methods=['DELETE'])
def delete_reserva():
  id = req.args.get('id')

  result = db_reserva.delete(id)

  return res(jsonify(result), result['status'])

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")
