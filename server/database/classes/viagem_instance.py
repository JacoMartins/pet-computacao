from datetime import datetime
import sqlite3 as sql

from database.schemas import schema_viagem
from utils.response_message import response_message

class viagem:
  def __init__(self, database_url):
    self.database_url = database_url
    self.table_name = 'viagem'

  def insert(self, data):
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

  def update(self, id, data):
    schemed_data = schema_viagem(
      id_linha=data['id_linha'],
      data=data['data'],
      iniciou_as=data['iniciou_as'],
      terminou_as=data['terminou_as'],
      atualizado_em=datetime.now(),
      pago_dinheiro=data['pago_dinheiro'],
      pago_meia=data['pago_meia'],
      gratuidade=data['gratuidade'],
      assentos_disponiveis=data['assentos_disponiveis'],
    ).get_dict()  

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE {self.table_name}
        SET id_linha = {schemed_data["id_linha"]},
        data = '{schemed_data["data"]}',
        iniciou_as = '{schemed_data["iniciou_as"]}',
        terminou_as = '{schemed_data["terminou_as"]}',
        atualizado_em = '{schemed_data["atualizado_em"]}',
        pago_dinheiro = {schemed_data["pago_dinheiro"]},
        pago_meia = {schemed_data["pago_meia"]},
        gratuidade = {schemed_data["gratuidade"]},
        assentos_disponiveis = {schemed_data["assentos_disponiveis"]}
        WHERE id = {id};
        ''')

    result = schema_viagem(
      id=id,
      id_linha=data['id_linha'],
      data=data['data'],
      iniciou_as=data['iniciou_as'],
      terminou_as=data['terminou_as'],
      atualizado_em=datetime.now(),
      pago_dinheiro=data['pago_dinheiro'],
      pago_meia=data['pago_meia'],
      gratuidade=data['gratuidade'],
      assentos_disponiveis=data['assentos_disponiveis'],
    ).get_dict()

    return response_message(status=200, message="Viagem atualizada com sucesso", data=result)

  def delete(self, id):
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

    return response_message(status=200, message="Viagem deletada com sucesso").get_dict()

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM {self.table_name}
        ''')

      data = cursor.fetchall()

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

    return response_message(status=200, message="Viagens encontradas com sucesso", data=result).get_dict()
  
  def get_where(self, column, operator, value):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      
      queries = [
        f'''
        SELECT FROM TABLE {self.table_name}
        WHERE {column} {operator} {value};
        '''
      ]

      for query in queries:
        cursor.execute(query)
      
      data = cursor.fetchall()

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

      return response_message(status=200, message="Paradas encontradas", data=result).get_dict()
      