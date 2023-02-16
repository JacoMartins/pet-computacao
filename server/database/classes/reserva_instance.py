from datetime import datetime
import sqlite3 as sql

from database.db_global import global_functions
from database.schemas import schema_reserva
from utils.response_message import response_message

class reserva:
  def __init__(self, database_url):
    self.database_url = database_url
    self.table_name = 'reserva'

  def insert(self, data):
    viagem_exists = global_functions(self.database_url).select({
      'attribute': 'id',
      'from': 'viagem',
      'where': {
        'column': 'id',
        'operator': '=',
        'value': data['id_viagem']
      }
    })

    if not viagem_exists:
      return response_message(status=404, message="Impossível criar reserva: Viagem não encontrada").get_dict()

    result = schema_reserva(
      id_viagem=data['id_viagem'],
      assento=data['assento'],
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO {self.table_name}
        (id_viagem, assento, criado_em, atualizado_em)
        VALUES (
          {result['id_viagem']},
          {result['assento']},
          '{result['criado_em']}',
          '{result['atualizado_em']}'
          );
        ''')

      result['id'] = cursor.lastrowid
    
    return response_message(status=200, message='Reserva criada com sucesso', data=result).get_dict()
  
  def get(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM {self.table_name}
        WHERE id = {id}
        ''')

      data = cursor.fetchone()

      if not data:
        return response_message("Linha não encontrada").get_dict()

      result = schema_reserva(
        id=data[0],
        id_viagem=data[1],
        assento=data[2],
        criado_em=data[3],
        atualizado_em=data[4]
      ).get_dict()

      return response_message(status=200, message='Reserva encontrada com sucesso', data=result).get_dict()

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM {self.table_name}
        ''')

      data = cursor.fetchall()

      if len(data) == 0:
        return response_message(status=200, message="Nenhuma reserva encontrada").get_dict()
      elif not data:
        return response_message(status=500, message="Ocorrou um erro interno.").get_dict()

      result = [schema_reserva(
        id=i[0],
        id_viagem=i[1],
        assento=i[2],
        criado_em=i[3],
        atualizado_em=i[4]
      ).get_dict() for i in data]

    return response_message(status=200, message=f"{len(result)} reservas encontradas com sucesso", data=result).get_dict()

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
        return response_message(status=200, message="Nenhuma reserva encontrada").get_dict()
      elif not data:
        return response_message(status=500, message="Ocorrou um erro interno.").get_dict()

      result = [schema_reserva(
        id=i[0],
        id_viagem=i[1],
        assento=i[2],
        criado_em=i[3],
        atualizado_em=i[4]
      ).get_dict() for i in data]
      
      return response_message(status=200, message=f"{len(result)} reservas encontradas", data=result).get_dict()
      
  def update(self, id, data):
    try:
      reserva_exists = self.get(id)['data']
    except KeyError:
      return response_message(status=404, message="Impossível realizar ação: Reserva não encontrada").get_dict()

    result = schema_reserva(
      id_viagem=data['id_viagem'],
      assento=data['assento'],
      criado_em=reserva_exists['criado_em'],
      atualizado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE {self.table_name}
        SET id_viagem = {result['id_viagem']},
        assento = {result['assento']},
        atualizado_em = '{result['atualizado_em']}'
        WHERE id = {id}
        ''')

    result['id'] = int(id)

    return response_message(status=200, message='Reserva atualizada com sucesso', data=result).get_dict()

  def delete(self, id):
    try:
      result = self.get(id)['data']
    except KeyError:
      return response_message(status=404, message="Impossível realizar ação: Reserva não encontrada").get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()

      queries = [
        f'''
        DELETE FROM {self.table_name}
        WHERE id = {id}
        '''
      ]

      for query in queries:
        cursor.execute(query)

    return response_message(status=204, message="Parada deletada com sucesso", data=result).get_dict()