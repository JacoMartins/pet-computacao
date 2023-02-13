from module_linha import linha
from module_viagem import viagem_de_onibus
from module_reserva import reserva
from module_parada import parada

import sqlite3 as sql

class simple:
  def __init__(self, database_url):
    self.connection = sql.connect(database_url)
    self.cursor = self.connection.cursor()
    self.linha = linha()
    self.viagem = viagem_de_onibus()
    self.reserva = reserva()
    self.parada = parada()

    self.reset_to_default = [
      '''
        DROP TABLE IF EXISTS linha;  
        CREATE TABLE IF NOT EXISTS linha (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          cod INTEGER, nome TEXT,
          distancia_km INTEGER,
          criado_em TEXT,
          atualizado_em TEXT NULL,
          destino TEXT,
          valor_dinheiro DECIMAL(10,2),
          valor_meia DECIMAL(10,2),
          capacidade_de_assento INTEGER
        );
      ''',
      
      '''
        DROP TABLE IF EXISTS viagem;
        CREATE TABLE IF NOT EXISTS viagem (
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
      ''',

      '''
        DROP TABLE IF EXISTS reserva;
        CREATE TABLE IF NOT EXISTS reserva (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          id_viagem INTEGER,
          assento INTEGER,
          criado_em TEXT,
          atualizado_em TEXT NULL,
          FOREIGN KEY (id_viagem) REFERENCES viagem(id)
        ); 
      ''',

      '''
        DROP TABLE IF EXISTS parada;
        CREATE TABLE IF NOT EXISTS parada (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          id_linha INTEGER,
          hora_de_parada TEXT,
          parada TEXT,
          criado_em TEXT,
          atualizado_em TEXT NULL,
          FOREIGN KEY (id_linha) REFERENCES linha(id)
        );
      '''
    ]

  def default_migration(self):
    for migration in self.reset_to_default:
      self.cursor.execute(migration)
    self.connection.commit()
