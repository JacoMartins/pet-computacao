from datetime import datetime
import sqlite3 as sql

class parada:
  def __init__(self, database_url):
    self.database_url = database_url

  def insert(self, data):
    result = {
      "id_linha": data['id_linha'],
      "hora_de_parada": data['hora_da_parada'],
      "parada": data['parada'],
      "criado_em": datetime.now(),
      "atualizado_em": data['atualizado_em'],
    }

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO paradaself.
        (id_linha, hora_de_parada, parada, criado_em, atualizado_em)
        VALUES (
          {result.id_linha},
          '{result.hora_de_parada}',
          '{result.parada}',
          '{result.criado_em}',
          '{result.atualizado_em}'
          );
        ''')
    return result.__dict__

  def get(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM parada
        WHERE id = {id}
        ''')
      return cursor.fetchone()

  def update(self, id, data):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE parada
        SET id_linha = {data["id_linha"]},
        hora_de_parada = '{data["hora_de_parada"]}',
        parada = '{data["parada"]}',
        atualizado_em = '{data["atualizado_em"]}'
        WHERE id = {id}
        ''')
    return self.__dict__

  def delete(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        DELETE FROM parada
        WHERE id = {id}
        ''')
    return self.__dict__

  def get_all(self):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM parada
        ''')
      return cursor.fetchall().__dict__