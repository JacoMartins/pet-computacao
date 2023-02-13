from datetime import datetime
import sqlite3 as sql

class reserva:
  def __init__(self, database_url):
    self.database_url = database_url

  def insert(self, data):
    result = {
        'id_viagem': data['id_viagem'],
        'assento': data['assento'],
        'criado_em': datetime.now(),
        'atualizado_em': data['atualizado_em']
    }
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO reserva
        (id_viagem, assento, criado_em, atualizado_em)
        VALUES (
          {result['id_viagem']},
          {result['assento']},
          '{result['criado_em']}',
          '{result['atualizado_em']}'
          );
        ''')
    return result
  
  def get(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM reserva
        WHERE id = {id}
        ''')
      return cursor.fetchone()

  def update(self, id, data):
    result = {
        'id_viagem': data['id_viagem'],
        'assento': data['assento'],
        'atualizado_em': data['atualizado_em']
    }
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE reserva
        SET id_viagem = {result['id_viagem']},
        assento = {result['assento']},
        atualizado_em = '{result['atualizado_em']}'
        WHERE id = {id}
        ''')
    return result

  def delete(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        DELETE FROM reserva
        WHERE id = {id}
        ''')

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM reserva
        ''')
      return cursor.fetchall()
