import sqlite3 as sql
import os

from utils import response_message

class global_functions:
  def __init__(self, database_url):
    self.database_url = database_url
    self.root_folder = os.listdir('.')

  def select(self, select_object:dict):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()

      queries = [
        f'''
        SELECT {select_object['attribute']} FROM {select_object['from']}
        WHERE {select_object['where']['column']} {select_object['where']['operator']} {select_object['where']['value']};
        '''
      ]

      try:
        for query in queries:
          cursor.execute(query)

      except sql.OperationalError as error:
        return response_message(status=500, message=f"Erro na query: {error}").get_dict()
      
      data = cursor.fetchall()

    return data

  def create_tables(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      queries = [
        '''
          CREATE TABLE IF NOT EXISTS
          linha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cod INTEGER,
            nome TEXT,
            distancia_km INTEGER,
            criado_em TEXT,
            atualizado_em TEXT NULL,
            destino TEXT,
            valor_dinheiro DECIMAL(10, 2),
            valor_meia DECIMAL(10, 2),
            capacidade_de_assento INTEGER
          );
        ''',
        '''
          CREATE TABLE IF NOT EXISTS
          parada (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_linha INTEGER,
            hora_de_parada TEXT,
            parada TEXT,
            criado_em TEXT,
            atualizado_em TEXT NULL,
            FOREIGN KEY (id_linha) REFERENCES linha(id)
          );
        ''',
        '''
          CREATE TABLE IF NOT EXISTS
          reserva (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_viagem INTEGER,
            assento INTEGER,
            criado_em TEXT,
            atualizado_em TEXT NULL,
            FOREIGN KEY (id_viagem) REFERENCES viagem(id)
          );
        ''',
        '''
          CREATE TABLE IF NOT EXISTS
          viagem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_linha INTEGER,
            data TEXT,
            iniciou_as TEXT,
            terminou_as TEXT,
            criado_em TEXT,
            atualizado_em TEXT NULL,
            pago_dinheiro INTEGER,
            pago_meia INTEGER,
            gratuidade INTEGER,
            assentos_disponiveis TEXT,
            FOREIGN KEY (id_linha) REFERENCES linha(id)
          );
        '''
      ]
  
      for query in queries:
        cursor.execute(query)

  def db_config(self):
    if 'database.db' not in self.root_folder:
      os.system('touch database.db')
      self.create_tables()
