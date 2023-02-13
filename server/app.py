from flask import Flask, request as req, jsonify, make_response as res
from module_linha import linha
from module_viagem import viagem_de_onibus
from module_parada import parada
from module_reserva import reserva

app = Flask(__name__)

db_linha = linha('database.db')
db_viagem = viagem_de_onibus('database.db')
db_parada = parada('database.db')
db_reserva = reserva('database.db')

@app.route("/")
def index():
  return "Bem-vindo ao sistema de reservas de linha de ônibus do Câmpus UFC."

# Linhas

@app.route("/linha", methods=['GET'])
def get_linha():
  result = db_linha.get_all()

  return jsonify(result)

@app.route("/linha", methods=['POST'])
def post_linha():
  data = req.get_json()

  result = db_linha.insert(data)

  return res(jsonify(result), 201)

# Viagens

@app.route('/viagem', methods=['GET'])
def get_viagem():
  result = db_viagem.get_all()

  return result

@app.route("/viagem", methods=['POST'])
def post_viagem():
  data = req.get_json()

  result = db_viagem.insert(data)

  return res(jsonify(result), 201)

@app.route("/viagem/<id>", methods=['PUT'])
def put_viagem(id):
  data = req.get_json()

  result = db_viagem.update(id)

  return res(jsonify(result), 200)

if __name__ == "__main__":
  app.run(debug=True)
