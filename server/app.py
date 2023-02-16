from flask import Flask, request as req, jsonify, make_response as res

from database.classes.linha_instance import linha
from database.classes.viagem_instance import viagem
from database.classes.parada_instance import parada
from database.classes.reserva_instance import reserva

from database.db_global import global_functions

banco = 'database.db'

app = Flask(__name__)

db_global = global_functions(banco)
db_linha = linha(banco)
db_viagem = viagem(banco)
db_parada = parada(banco)
db_reserva = reserva(banco)

db_global.db_config()

@app.route("/")
def index():
  return "Bem-vindo ao sistema de reservas de linha de ônibus do Câmpus UFC."

# Linhas

@app.route("/linha", methods=['GET'])
def get_linha():
  if req.args.get('id'):
    result = db_linha.get(req.args.get('id'))

    return res(jsonify(result), result['status'])
    
  result = db_linha.get_all()

  return res(jsonify(result), result['status'])


@app.route("/linha", methods=['POST'])
def post_linha():
  data = req.get_json()

  result = db_linha.insert(data)

  return res(jsonify(result), result['status'])

@app.route("/linha", methods=['PUT'])
def put_linha():
  id = req.args.get('id')
  data = req.get_json()

  result = db_linha.update(id, data)

  return res(jsonify(result), result['status'])

@app.route("/linha", methods=['DELETE'])
def delete_linha():
  id = req.args.get('id')

  result = db_linha.delete(id)

  return res(jsonify(result), result['status'])

# Viagens

@app.route('/viagem', methods=['GET'])
def get_viagem():
  if req.args.get('id'):
    result = db_viagem.get(req.args.get('id'))
    return res(jsonify(result), result['status'])
  if req.args.get('linha'):
    result = db_viagem.get_where('id_linha', '=', req.args.get('linha'))
    return res(jsonify(result), result['status'])

  result = db_viagem.get_all()
  return result

@app.route("/viagem", methods=['POST'])
def post_viagem():
  data = req.get_json()

  result = db_viagem.insert(data)

  return res(jsonify(result), result['status'])

@app.route("/viagem", methods=['PUT'])
def put_viagem():
  id = req.args.get('id')
  data = req.get_json()

  result = db_viagem.update(id, data)

  return res(jsonify(result), result['status'])

@app.route("/viagem", methods=['DELETE'])
def delete_viagem():
  id = req.args.get('id')

  result = db_viagem.delete(id)

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
  app.run(debug=True)
