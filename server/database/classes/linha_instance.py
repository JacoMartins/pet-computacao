from datetime import datetime
import sqlite3 as sql

from database.schemas import schema_linha
from utils.response_message import response_message

class linha:
  def __init__(self, database_url):
    self.database_url = database_url
    self.table_name = 'linha'

  def insert(self, data):
    result = schema_linha(
      cod=data['cod'],
      nome=data['nome'],
      distancia_km=data['distancia_km'],
      destino=data['destino'],
      valor_dinheiro=data['valor_dinheiro'],
      capacidade_de_assento=data['capacidade_de_assento']
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO {self.table_name}
        (cod, nome, distancia_km, criado_em, atualizado_em, destino, valor_dinheiro, valor_meia, capacidade_de_assento)
        VALUES ( 
          {result["cod"]},
          '{result["nome"]}',
          {result["distancia_km"]},
          '{result["criado_em"]}',
          '{result["atualizado_em"]}',
          '{result["destino"]}',
          {result["valor_dinheiro"]},
          {result["valor_meia"]},
          {result["capacidade_de_assento"]});
        ''')

    return response_message(status=201, message="Linha inserida com sucesso", data=result).get_dict()
  
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
      
      result = schema_linha(
        id=data[0],
        cod=data[1],
        nome=data[2],
        distancia_km=data[3],
        criado_em=data[4],
        atualizado_em=data[5],
        destino=data[6],
        valor_dinheiro=data[7],
        valor_meia=data[8],
        capacidade_de_assento=data[9]
      ).get_dict()

      return response_message(status=200, message="Linha encontrada", data=result).get_dict()

  def update(self, id, data):
    schemed_data = schema_linha(
      cod=data['cod'],
      nome=data['nome'],
      distancia_km=data['distancia_km'],
      atualizado_em=datetime.now(),
      destino=data['destino'],
      valor_dinheiro=data['valor_dinheiro'],
      capacidade_de_assento=data['capacidade_de_assento']
    ).get_dict()

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE {self.table_name}
        SET cod = {schemed_data["cod"]},
        nome = '{schemed_data["nome"]}',
        distancia_km = {schemed_data["distancia_km"]},
        atualizado_em = '{schemed_data["atualizado_em"]}',
        destino = '{schemed_data["destino"]}',
        valor_dinheiro = {schemed_data["valor_dinheiro"]},
        valor_meia = {schemed_data["valor_meia"]},
        capacidade_de_assento = {schemed_data["capacidade_de_assento"]}
        WHERE id = {id};
      ''')

    result = schema_linha(
      id=id,
      cod=data['cod'],
      nome=data['nome'],
      distancia_km=data['distancia_km'],
      destino=data['destino'],
      valor_dinheiro=data['valor_dinheiro'],
      capacidade_de_assento=data['capacidade_de_assento']
    ).get_dict()
      
    return response_message(status=200, message="Linha atualizada com sucesso", data=result).get_dict()

  def delete(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()

      queries = [
        f'''
          DELETE FROM viagem
          WHERE id_linha = {id};
        ''',
        f'''
          DELETE FROM reserva
          WHERE id_viagem IN (
            SELECT id FROM viagem
            WHERE id_linha = {id}
          );
        ''',
        f'''
          DELETE FROM parada
          WHERE id_linha = {id};
        ''',
        f'''
          DELETE FROM {self.table_name}
          WHERE id = {id};
        '''
      ]

      for query in queries:
        cursor.execute(query)

    return response_message(status=204, message="Linha deletada com sucesso").get_dict()

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

      result = [schema_linha(
        id=i[0],
        cod=i[1],
        nome=i[2],
        distancia_km=i[3],
        criado_em=i[4],
        atualizado_em=i[5],
        destino=i[6],
        valor_dinheiro=i[7],
        valor_meia=i[8],
        capacidade_de_assento=i[9]
      ).get_dict() for i in data]

    return response_message(status=200, message="Linha encontrada com sucesso", data=result).get_dict()
  
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

      result = [schema_linha(
        id=i[0],
        cod=i[1],
        nome=i[2],
        distancia_km=i[3],
        criado_em=i[4],
        atualizado_em=i[5],
        destino=i[6],
        valor_dinheiro=i[7],
        valor_meia=i[8],
        capacidade_de_assento=i[9]
      ).get_dict() for i in data]

      
      return response_message(status=200, message="Paradas encontradas", data=result).get_dict()