from datetime import datetime
import sqlite3 as sql

from database.schemas import schema_parada
from utils.response_message import response_message

class parada():
  def __init__(self, database_url):
    self.database_url = database_url
    self.table_name = 'parada'

  def insert(self, data):
    result = schema_parada(
      id_linha=data['id_linha'],
      hora_de_parada=data['hora_de_parada'],
      parada=data['parada'],
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO {self.table_name}
        (id_linha, hora_de_parada, parada, criado_em, atualizado_em)
        VALUES (
          {result.id_linha},
          '{result.hora_de_parada}',
          '{result.parada}',
          '{result.criado_em}',
          '{result.atualizado_em}'
          );
        ''')
    return response_message(status=201, message="Parada inserida com sucesso", data=result).get_dict()

  def get(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM {self.table_name}
        WHERE id = {id}
        ''')

      data = cursor.fetchone()

      if not data:
        return response_message(status=404, message="Linha não encontrada").get_dict()

      result = schema_parada(
        id=data[0],
        id_linha=data[1],
        hora_de_parada=data[2],
        parada=data[3],
        criado_em=data[4],
        atualizado_em=data[5]
      ).get_dict()

    return response_message(status=200, message="Parada encontrada", data=result).get_dict()

  def update(self, id, data):
    schemed_data = schema_parada(
      id_linha=data['id_linha'],
      hora_de_parada=data['hora_de_parada'],
      parada=data['parada'],
      atualizado_em=datetime.now()
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE {self.table_name}
        SET id_linha = {schemed_data["id_linha"]},
        hora_de_parada = '{schemed_data["hora_de_parada"]}',
        parada = '{schemed_data["parada"]}',
        atualizado_em = '{schemed_data["atualizado_em"]}'
        WHERE id = {id}
        ''')

    result = schema_parada(
      id=id,
      id_linha=data['id_linha'],
      hora_de_parada=data['hora_de_parada'],
      parada=data['parada'],
      atualizado_em=data['atualizado_em']
    ).get_dict()

    return response_message(status=200,message="Parada atualizada com sucesso", data=result).get_dict()

  def delete(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()

      queries = [
        f'''
        DELETE FROM {self.table_name}
        WHERE id = {id}
        ''',
      ]

      for query in queries:
        cursor.execute(query)
    
    return response_message(status=204, message="Parada deletada com sucesso").get_dict()

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM {self.table_name}
        ''')
      
      data = cursor.fetchall()

      if len(data) == 0:
        return response_message(status=200, message="Nenhuma linha encontrada").get_dict()
      elif not data:
        return response_message(status=500, message="Ocorrou um erro interno.").get_dict()

      result = [schema_parada(
        id=i[0],
        id_linha=i[1],
        hora_de_parada=i[2],
        parada=i[3],
        criado_em=i[4],
        atualizado_em=i[5],
      ).get_dict() for i in data]

    return response_message(status=200 ,message="Paradas encontradas", data=result).get_dict()

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

      result = [schema_parada(
        id=i[0],
        id_linha=i[1],
        hora_de_parada=i[2],
        parada=i[3],
        criado_em=i[4],
        atualizado_em=i[5],
      ).get_dict() for i in data]
      
      return response_message(status=200, message="Paradas encontradas", data=result).get_dict()
      