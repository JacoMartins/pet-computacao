import sqlite3 as sql
import os

root_folder = os.listdir('.')

db = sql.connect('database.db')
cursor = db.cursor()

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

def create_tables():
  for query in queries:
    cursor.execute(query)

def db_config():
  if 'database.db' not in root_folder:
    os.system('touch database.db')
    create_tables()
