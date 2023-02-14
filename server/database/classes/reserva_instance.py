from datetime import datetime
import sqlite3 as sql

from database.schemas import schema_reserva
from utils.response_message import response_message

class reserva:
  def __init__(self, database_url):
    self.database_url = database_url
    self.table_name = 'reserva'

  def insert(self, data):
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

  def update(self, id, data):
    schemed_data = {
        'id_viagem': data['id_viagem'],
        'assento': data['assento'],
        'atualizado_em': datetime.now()
    }
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE {self.table_name}
        SET id_viagem = {schemed_data['id_viagem']},
        assento = {schemed_data['assento']},
        atualizado_em = '{schemed_data['atualizado_em']}'
        WHERE id = {id}
        ''')

    result = schema_reserva(
      id=id,
      id_viagem=data['id_viagem'],
      assento=data['assento'],
      criado_em=data['criado_em'],
      atualizado_em=data['atualizado_em']
    ).get_dict()

    return response_message(status=200, message='Reserva atualizada com sucesso', data=result).get_dict()

  def delete(self, id):
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

      result = [schema_reserva(
        id=i[0],
        id_viagem=i[1],
        assento=i[2],
        criado_em=i[3],
        atualizado_em=i[4]
      ).get_dict() for i in data]

    return response_message(status=200, message='Reservas encontradas com sucesso', data=result).get_dict()

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

      result = [schema_reserva(
        id=i[0],
        id_viagem=i[1],
        assento=i[2],
        criado_em=i[3],
        atualizado_em=i[4]
      ).get_dict() for i in data]
      
      return response_message(status=200, message="Paradas encontradas", data=result).get_dict()
      