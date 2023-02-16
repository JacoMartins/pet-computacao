from datetime import datetime
import sqlite3 as sql

from database.schemas import schema_viagem
from database.db_global import global_functions
from utils.response_message import response_message

class viagem:
  def __init__(self, database_url):
    self.database_url = database_url
    self.table_name = 'viagem'

  def insert(self, data):
    linha_exists = global_functions(self.database_url).select({
      'attribute': 'id',
      'from': 'linha',
      'where': {
        'column': 'id',
        'operator': '=',
        'value': data['id_linha']
      }
    })

    if not linha_exists:
      return response_message(status=404, message="Impossível criar viagem: Linha não encontrada").get_dict()

    result = schema_viagem(
      id_linha=data['id_linha'],
      data=data['data'],
      iniciou_as=data['iniciou_as'],
      terminou_as=data['terminou_as'],
      assentos_disponiveis=data['assentos_disponiveis'],
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO {self.table_name}
        (id_linha, data, iniciou_as, terminou_as, criado_em, atualizado_em, pago_dinheiro, pago_meia, gratuidade, assentos_disponiveis)
        VALUES (
          {result['id_linha']},
          '{result['data']}',
          '{result['iniciou_as']}',
          '{result['terminou_as']}',
          '{result['criado_em']}',
          '{result['atualizado_em']}',
          {result['pago_dinheiro']},
          {result['pago_meia']},
          {result['gratuidade']},
          {result['assentos_disponiveis']}
          );
        ''')

    result['id'] = cursor.lastrowid

    return response_message(status=201, message="Viagem inserida com sucesso", data=result).get_dict()
  
  def get(self, id):
    with sql.connect(self.database_url) as connection:
      db = connection.cursor()
      db.execute(f'''
        SELECT * FROM {self.table_name}
        WHERE id = {id}
        ''')

      data = db.fetchone()

      if not data:
        return response_message(status=404, message="Viagem não encontrada.").get_dict()

      result = schema_viagem(
        id=data[0],
        id_linha=data[1],
        data=data[2],
        iniciou_as=data[3],
        terminou_as=data[4],
        criado_em=data[5],
        atualizado_em=data[6],
        pago_dinheiro=data[7],
        pago_meia=data[8],
        gratuidade=data[9],
        assentos_disponiveis=data[10],
      ).get_dict()

      return response_message(status=200, message="Viagem encontrada com sucesso", data=result).get_dict()

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM {self.table_name}
        ''')

      data = cursor.fetchall()

      if len(data) == 0:
        return response_message(status=200, message=f"Nenhuma viagem encontrada").get_dict()
      elif not data:
        return response_message(status=500, message="Ocorrou um erro interno.").get_dict()

      result = [schema_viagem(
        id=i[0],
        id_linha=i[1],
        data=i[2],
        iniciou_as=i[3],
        terminou_as=i[4],
        criado_em=i[5],
        atualizado_em=i[6],
        pago_dinheiro=i[7],
        pago_meia=i[8],
        gratuidade=i[9],
        assentos_disponiveis=i[10],
      ).get_dict() for i in data]

    return response_message(status=200, message=f"{len(result)} viagens encontradas com sucesso", data=result).get_dict()

  def get_where(self, column, operator, value):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      
      queries = [
        f'''
        SELECT * FROM {self.table_name}
        WHERE {column} {operator} {value};
        '''
      ]

      try:
        for query in queries:
          cursor.execute(query)
      except sql.OperationalError as error:
        return response_message(status=500, message=f"Erro na query: {error}").get_dict()
      
      data = cursor.fetchall()

      if len(data) == 0:
        return response_message(status=200, message="Nenhuma viagem encontrada").get_dict()
      elif not data:
        return response_message(status=500, message="Ocorrou um erro interno.").get_dict()

      result = [schema_viagem(
        id=i[0],
        id_linha=i[1],
        data=i[2],
        iniciou_as=i[3],
        terminou_as=i[4],
        criado_em=i[5],
        atualizado_em=i[6],
        pago_dinheiro=i[7],
        pago_meia=i[8],
        gratuidade=i[9],
        assentos_disponiveis=i[10],
      ).get_dict() for i in data]

      return response_message(status=200, message=f"{len(result)} viagens encontradas", data=result).get_dict()
      
  def update(self, id, data):
    try:
      viagem_exists = self.get(id)['data']
    except KeyError:
      return response_message(status=404, message="Impossível realizar ação: Viagem não encontrada").get_dict()

    result = schema_viagem(
      id_linha=data['id_linha'],
      data=data['data'],
      iniciou_as=data['iniciou_as'],
      terminou_as=data['terminou_as'],
      criado_em=viagem_exists['criado_em'],
      atualizado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
      pago_dinheiro=data['pago_dinheiro'],
      pago_meia=data['pago_meia'],
      gratuidade=data['gratuidade'],
      assentos_disponiveis=data['assentos_disponiveis'],
    ).get_dict()  

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE {self.table_name}
        SET id_linha = {result["id_linha"]},
        data = '{result["data"]}',
        iniciou_as = '{result["iniciou_as"]}',
        terminou_as = '{result["terminou_as"]}',
        atualizado_em = '{result["atualizado_em"]}',
        pago_dinheiro = {result["pago_dinheiro"]},
        pago_meia = {result["pago_meia"]},
        gratuidade = {result["gratuidade"]},
        assentos_disponiveis = {result["assentos_disponiveis"]}
        WHERE id = {id};
        ''')

    result['id'] = int(id)

    return response_message(status=200, message="Viagem atualizada com sucesso", data=result).get_dict()

  def delete(self, id):
    try:
      result = self.get(id)['data']
    except KeyError:
      return response_message(status=404, message="Impossível realizar ação: Viagem não encontrada").get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()

      queries = [
        f'''
          DELETE FROM parada
          WHERE id = {id};
        ''',
        f'''
          DELETE FROM parada
          WHERE id = {id};
        ''',
        f'''
          DELETE FROM reserva
          WHERE id_viagem = {id};
        ''',
        f'''
          DELETE FROM {self.table_name}
          WHERE id = {id}
        '''
      ]

      for query in queries:
        cursor.execute(query)

    return response_message(status=200, message="Viagem deletada com sucesso", data=result).get_dict()