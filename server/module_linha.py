from datetime import datetime
import sqlite3 as sql

class linha:
  def __init__(self, database_url):
    self.database_url = database_url

  def insert(self, data):
    result = {
      "cod": data['cod'],
      "nome": data['nome'],
      "distancia_km": data['distancia_km'],
      "criado_em": datetime.now(),
      "atualizado_em": datetime.now(),
      "destino": data['destino'],
      "valor_dinheiro": data['valor_dinheiro'],
      "valor_meia": data['valor_dinheiro'] / 2,
      "capacidade_de_assento": data['capacidade_de_assento'],
    }

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO linha
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
    return self.__dict__
  
  def get(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM linha
        WHERE id = {id}
        ''')
      return cursor.fetchone()

  def update(self, id, data):
    result = {
      "cod": data['cod'],
      "nome": data['nome'],
      "distancia_km": data['distancia_km'],
      "criado_em": datetime.now(),
      "atualizado_em": datetime.now(),
      "destino": data['destino'],
      "valor_dinheiro": data['valor_dinheiro'],
      "valor_meia": data['valor_dinheiro'] / 2,
      "capacidade_de_assento": data['capacidade_de_assento'],
    }

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE linha
        SET cod = {result["cod"]},
        nome = '{result["nome"]}',
        distancia_km = {result["distancia_km"]},
        atualizado_em = '{result["atualizado_em"]}',
        destino = '{result["destino"]}',
        valor_dinheiro = {result["valor_dinheiro"]},
        valor_meia = {result["valor_meia"]},
        capacidade_de_assento = {result["capacidade_de_assento"]}
        WHERE id = {id};
      ''')
    return self.__dict__

  def delete(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        DELETE FROM viagem
        WHERE id_linha = {id};

        DELETE FROM reserva
        WHERE id_viagem IN (
          SELECT id FROM viagem
          WHERE id_linha = {id}
        );

        DELETE FROM parada
        WHERE id_linha = {id};
        
        DELETE FROM linha
        WHERE id = {id};
        ''')
    return self.__dict__

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM linha
        ''')
      return cursor.fetchall()
