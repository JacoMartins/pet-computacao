from datetime import datetime
import sqlite3 as sql

from database.db_global import global_functions
from database.schemas import schema_parada
from utils.response_message import response_message

class parada():
  def __init__(self, database_url):
    self.database_url = database_url
    self.table_name = 'parada'

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
      return response_message(status=404, message="Impossível realizar ação: Linha não encontrada").get_dict()

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
          {result['id_linha']},
          '{result['hora_de_parada']}',
          '{result['parada']}',
          '{result['criado_em']}',
          '{result['atualizado_em']}'
          );
        ''')

      result['id'] = cursor.lastrowid

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
        return response_message(status=404, message="Parada não encontrada").get_dict()

      result = schema_parada(
        id=data[0],
        id_linha=data[1],
        hora_de_parada=data[2],
        parada=data[3],
        criado_em=data[4],
        atualizado_em=data[5]
      ).get_dict()

    return response_message(status=200, message="Parada encontrada", data=result).get_dict()

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM {self.table_name}
        ''')
      
      data = cursor.fetchall()

      if len(data) == 0:
        return response_message(status=200, message="Nenhuma parada encontrada").get_dict()
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

    return response_message(status=200 ,message=f"{len(result)} paradas encontradas", data=result).get_dict()

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
        return response_message(status=200, message="Nenhuma parada encontrada").get_dict()
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
      
      return response_message(status=200, message=f"{len(result)} paradas encontradas", data=result).get_dict()
      
  def update(self, id, data):
    try:
      parada_exists = self.get(id)['data']
    except KeyError:
      return response_message(status=404, message="Impossível realizar ação: Parada não encontrada").get_dict()
    
    result = schema_parada(
      id_linha=data['id_linha'],
      hora_de_parada=data['hora_de_parada'],
      parada=data['parada'],
      criado_em=parada_exists['criado_em'],
      atualizado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE {self.table_name}
        SET id_linha = {result["id_linha"]},
        hora_de_parada = '{result["hora_de_parada"]}',
        parada = '{result["parada"]}',
        atualizado_em = '{result["atualizado_em"]}'
        WHERE id = {id}
        ''')

    result['id'] = int(id)

    return response_message(status=200,message="Parada atualizada com sucesso", data=result).get_dict()

  def delete(self, id):
    try:
      result = self.get(id)['data']
    except KeyError:
      return response_message(status=404, message="Impossível realizar ação: Parada não encontrada").get_dict()
    
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
    
    return response_message(status=204, message="Parada deletada com sucesso", data=result).get_dict()