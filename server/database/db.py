from database.simple import simple

simple = simple(
  database_url="database.db",
  schemas=[
    {
      "name": "usuario",
      "fields":{
        "id": [int, "PRIMARY KEY", "AUTOINCREMENT", "NOT NULL"],
        "nome_usuario": [str, "UNIQUE", "NOT NULL"],
        "nome": [str, "NOT NULL"],
        "senha": [str, "NOT NULL"],
        "email": [str, "NOT NULL"],
        "admin": [int, "NOT NULL"],
        "criado_em": [str, "NOT NULL"],
        "atualizado_em": [str, "NULL"]    
      }
    },

    {
      "name": "linha",
      "fields":{
        "id": [int, "PRIMARY KEY", "AUTOINCREMENT", "NOT NULL"],
        "cod": [str, "UNIQUE", "NOT NULL"],
        "nome": [str, "NOT NULL"],
        "valor_inteira": [float, "NOT NULL"],
        "valor_meia": [float, "NOT NULL"],
        "tipo": [str, "NOT NULL"],
        "capacidade_assento": [int, "NOT NULL"],
        "criado_em": [str, "NOT NULL"],
        "atualizado_em": [str, "NULL"]
      }
    },

    {
      "name": "sentido",
      "fields":{
        "id": [int, "PRIMARY KEY", "AUTOINCREMENT", "NOT NULL"],
        "id_linha": [int, "NOT NULL"],
        "sentido": [str, "NOT NULL"],
        "ponto_partida": [str, "NOT NULL"],
        "ponto_destino": [str, "NOT NULL"],
        "horario_inicio": [str, "NOT NULL"],
        "horario_fim": [str, "NOT NULL"],
        "criado_em": [str, "NOT NULL"],
        "atualizado_em": [str, "NULL"],

        "fk_linha": ['id_linha', 'linha(id)']
      }
    },

    {
      "name": "parada",
      "fields":{
        "id": [int, "PRIMARY KEY", "AUTOINCREMENT", "NOT NULL"],
        "id_linha": [int, "NOT NULL"],
        "id_sentido": [int, "NOT NULL"],
        "parada": [str, "NOT NULL"],
        "minutos": [int, "NOT NULL"],
        "criado_em": [str, "NOT NULL"],
        "atualizado_em": [str, "NULL"],

        "fk_linha": ['id_linha', 'linha(id)'],
        "fk_sentido": ['id_sentido', 'sentido(id)']
      }
    },

    {
      "name": "viagem",
      "fields":{
        "id": [int, "PRIMARY KEY", "AUTOINCREMENT", "NOT NULL"],
        "id_linha": [int, "NOT NULL"],
        "id_sentido": [int, "NOT NULL"],
        "data": [str, "NOT NULL"],
        "origem": [str, "NOT NULL"],
        "destino": [str, "NOT NULL"],
        "horario_partida": [str, "NOT NULL"],
        "horario_chegada": [str, "NULL"],
        "pago_inteira": [int, "NOT NULL"],
        "pago_meia": [int, "NOT NULL"],
        "gratuidade": [int, "NOT NULL"],
        "assentos_disponiveis": [int, "NOT NULL"],
        "assentos_ocupados": [int, "NOT NULL"],
        "criado_em": [str, "NOT NULL"],
        "atualizado_em": [str, "NULL"],

        "fk_linha": ['id_linha', 'linha(id)'],
        "fk_sentido": ['id_sentido', 'sentido(id)']
      }
    },

    {
      "name": "reserva",
      "fields":{
        "id": [int, "PRIMARY KEY", "AUTOINCREMENT", "NOT NULL"],
        "id_viagem": [int, "NOT NULL"],
        "id_usuario": [int, "NOT NULL"],
        "assento": [int, "NOT NULL"],
        "forma_pagamento": [str, "NOT NULL"],
        "criado_em": [str, "NOT NULL"],
        "atualizado_em": [str, "NULL"],

        "fk_viagem": ['id_viagem', 'viagem(id)'],
        "fk_usuario": ['id_usuario', 'usuario(id)']
      }
    }
  ]
)