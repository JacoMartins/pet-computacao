from flask import Flask, request as req, jsonify, make_response as res
from flask_cors import CORS, cross_origin
from datetime import datetime
from utils.response_message import response_message
from utils.strip_accents import strip_accents
import bcrypt

from database.db import simple

simple.setup()
salt = bcrypt.gensalt()

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def index():
  return "Bem-vindo ao sistema de reservas de linha de ônibus do Câmpus UFC."

# Linhas

@app.route("/linha", methods=['GET'])
def get_linha():
  if req.args.get('id'):
    result = simple.linha.get_one(where={
      'field': 'id',
      'operator': '=',
      'value': req.args.get('id')
    })

    return res(jsonify(result), result['status'])
    
  result = simple.linha.get_all()

  return res(jsonify(result), result['status'])

@app.route("/linha_sentidos", methods=['GET'])
def get_linha_sentidos():
  if(req.args.get('page')):
    result = simple.linha.get_many(pagination={
      'page': req.args.get('page'),
      'limit': 15
    })

    if result['data']:
      for linha in result['data']:
        linha['sentidos'] = simple.sentido.get_many(where={
          'field': 'id_linha',
          'operator': '=',
          'value': linha['id']
        })['data']
  else:
    result = simple.linha.get_all()

    if result['data']:
      for linha in result['data']:
        linha['sentidos'] = simple.sentido.get_many(where={
          'field': 'id_linha',
          'operator': '=',
          'value': linha['id']
        })['data']

  return res(jsonify(result), result['status'])

@app.route("/search_linha", methods=['GET'])
def get_search_linha():
  query, page = req.args.get('query'), req.args.get('page')

  if query and page:
    result = simple.linha.get_many(where={
      "OR": [
        {
          'field': 'nome',
          'operator': 'LIKE',
          'value': f'%{req.args.get("query")}%'
        },

        {
          'field': 'cod',
          'operator': 'LIKE',
          'value': f'%{req.args.get("query")}%'
        },

        {
          'field': 'tipo',
          'operator': 'LIKE',
          'value': f'%{req.args.get("query")}%'
        }
      ]
    }, pagination={
      'page': req.args.get('page'),
      'limit': 15
    })

    try: 
      if result['data']:
        for linha in result['data']:
          linha['sentidos'] = simple.sentido.get_many(where={
            'field': 'id_linha',
            'operator': '=',
            'value': linha['id']
          })['data']
    except KeyError as e:
      result = response_message(status=200, message="Nenhuma linha encontrada.", data=[]).get_dict()
      
  else:
    result = simple.linha.get_many(where={
      "OR": [
        {
          'field': 'nome',
          'operator': 'LIKE',
          'value': f'%{req.args.get("query")}%'
        },

        {
          'field': 'cod',
          'operator': 'LIKE',
          'value': f'%{req.args.get("query")}%'
        },

        {
          'field': 'tipo',
          'operator': 'LIKE',
          'value': f'%{req.args.get("query")}%'
        }
      ]
    })
    
    try:
      if result['data']:
        for linha in result['data']:
          linha['sentidos'] = simple.sentido.get_many(where={
            'field': 'id_linha',
            'operator': '=',
            'value': linha['id']
          })['data']
    except KeyError as e:
      result = response_message(status=200, message="Nenhuma linha encontrada.", data=[]).get_dict()

  return res(jsonify(result), result['status'])

@app.route("/linha_count", methods=['GET'])
def get_linha_count():
  result = simple.linha.select_all(count='*')[0][0]

  return res(jsonify(result))

@app.route("/linha", methods=['POST'])
def post_linha():
  data = req.get_json()
  data['criado_em'] = datetime.now().isoformat()
  data['atualizado_em'] = datetime.now().isoformat()

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

  data['atualizado_em'] = datetime.now().isoformat()

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

  elif req.args.get('linha'):
    result = simple.viagem.get_many(where={
      'field': 'id_linha',
      'operator': '=',
      'value': req.args.get('linha')
    })

    return res(jsonify(result), result['status'])

  elif req.args.get('sentido'):
    result = simple.viagem.get_many(where={
      'field': 'id_sentido',
      'operator': '=',
      'value': req.args.get('sentido')
    })

    return res(jsonify(result), result['status'])
  
  elif req.args.get('linha') and req.args.get('sentido'):
    result = simple.viagem.get_many(where={
      'AND': [
        {
          'field': 'id_linha',
          'operator': '=',
          'value': req.args.get('linha')
        },
        {
          'field': 'id_sentido',
          'operator': '=',
          'value': req.args.get('sentido')
        }
      ]
    })

    return res(jsonify(result), result['status'])
    
  result = simple.viagem.get_all()

  return res(jsonify(result), result['status'])

@app.route("/viagem", methods=['POST'])
def post_viagem():
  data = req.get_json()
  data['criado_em'] = datetime.now().isoformat()
  data['atualizado_em'] = datetime.now().isoformat()

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

  data['atualizado_em'] = datetime.now().isoformat()

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
    result = simple.parada.get_one(where={
      'field': 'id',
      'operator': '=',
      'value': req.args.get('id')
    })

    return res(jsonify(result), result['status'])

  if req.args.get('linha') and req.args.get('sentido'):
    result = simple.parada.get_many(where={
      'AND': [
        {
          'field': 'id_linha',
          'operator': '=',
          'value': req.args.get('linha')
        },
        {
          'field': 'id_sentido',
          'operator': '=',
          'value': req.args.get('sentido')
        }
      ]
    })

    return res(jsonify(result), result['status'])

  elif req.args.get('sentido'):
    result = simple.parada.get_one(where={
      'field': 'id_sentido',
      'operator': '=',
      'value': req.args.get('sentido')
    })

    return res(jsonify(result), result['status'])
    
  result = simple.parada.get_all()

  return res(jsonify(result), result['status'])

@app.route("/parada", methods=['POST'])
def post_parada():
  data = req.get_json()
  data['criado_em'] = datetime.now().isoformat()
  data['atualizado_em'] = datetime.now().isoformat()

  result = simple.parada.insert(**data)

  return res(jsonify(result), result['status'])

@app.route("/parada", methods=['PUT'])
def put_parada():
  id = req.args.get('id')
  data = req.get_json()

  data['criado_em'] = simple.parada.get_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })['data']['criado_em']

  data['atualizado_em'] = datetime.now().isoformat()

  result = simple.parada.update_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  }, data=data)

  return res(jsonify(result), result['status'])

@app.route("/parada", methods=['DELETE'])
def delete_parada():
  id = req.args.get('id')

  result = simple.parada.delete_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })

  return res(jsonify(result), result['status'])

@app.route('/reserva', methods=['GET'])
def get_reserva():
  if req.args.get('id'):
    result = simple.reserva.get_one(where={
      'field': 'id',
      'operator': '=',
      'value': req.args.get('id')
    })

    return res(jsonify(result), result['status'])

  elif req.args.get('usuario'):
    result = simple.reserva.get_one(where={
      'field': 'id_usuario',
      'operator': '=',
      'value': req.args.get('usuario')
    })

    return res(jsonify(result), result['status'])

  elif req.args.get('viagem'):
    result = simple.reserva.get_one(where={
      'field': 'id_sentido',
      'operator': '=',
      'value': req.args.get('viagem')
    })

    return res(jsonify(result), result['status'])
    
  result = simple.parada.get_all()

  return res(jsonify(result), result['status'])

@app.route("/reserva", methods=['POST'])
def post_reserva():
  data = req.get_json()
  data['criado_em'] = datetime.now().isoformat()
  data['atualizado_em'] = datetime.now().isoformat()

  result = simple.reserva.insert(**data)

  return res(jsonify(result), result['status'])

@app.route("/reserva", methods=['PUT'])
def put_reserva():
  id = req.args.get('id')
  data = req.get_json()

  data['criado_em'] = simple.reserva.get_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })['data']['criado_em']

  data['atualizado_em'] = datetime.now().isoformat()

  result = simple.reserva.update_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  }, data=data)

  return res(jsonify(result), result['status'])

@app.route("/reserva", methods=['DELETE'])
def delete_reserva():
  id = req.args.get('id')

  result = simple.reserva.delete_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })

  return res(jsonify(result), result['status'])

# Sentido
@app.route('/sentido', methods=['GET'])
def get_sentido():
  if req.args.get('id'):
    result = simple.sentido.get_one(where={
      'field': 'id',
      'operator': '=',
      'value': req.args.get('id')
    })

    return res(jsonify(result), result['status'])

  if req.args.get('linha'):
    result = simple.sentido.get_many(where={
      'field': 'id_linha',
      'operator': '=',
      'value': req.args.get('linha')
    })

    return res(jsonify(result), result['status'])
    
  result = simple.sentido.get_all()

  return res(jsonify(result), result['status'])

@app.route("/sentido", methods=['POST'])
def post_sentido():
  data = req.get_json()
  data['criado_em'] = datetime.now().isoformat()
  data['atualizado_em'] = datetime.now().isoformat()

  result = simple.sentido.insert(**data)

  return res(jsonify(result), result['status'])

@app.route("/sentido", methods=['PUT'])
def put_sentido():
  id = req.args.get('id')
  data = req.get_json()

  data['criado_em'] = simple.sentido.get_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })['data']['criado_em']

  data['atualizado_em'] = datetime.now().isoformat()

  result = simple.sentido.update_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  }, data=data)

  return res(jsonify(result), result['status'])

@app.route("/sentido", methods=['DELETE'])
def delete_sentido():
  id = req.args.get('id')

  result = simple.sentido.delete_one(where={
    'field': 'id',
    'operator': '=',
    'value': id
  })

  return res(jsonify(result), result['status'])

# Usuário

@app.route('/usuario', methods=['POST'])
def post_usuario():
  data = req.get_json()
  data['criado_em'] = datetime.now().isoformat()
  data['atualizado_em'] = datetime.now().isoformat()
  data['admin'] = 0

  bytePassword = data['senha'].encode('utf-8')
  hashPassword = bcrypt.hashpw(bytePassword, salt)

  data['senha'] = hashPassword.decode('utf-8')

  result = simple.usuario.insert(**data)

  return res(jsonify(result), result['status'])

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")
