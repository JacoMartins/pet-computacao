from datetime import datetime
import sqlite3 as sql

class viagem_de_onibus:
  def __init__(self, database_url):
    self.database_url = database_url

  def insert(self, data):
    result = {
      'id_linha': data['id_linha'],
      'data': data['data'],
      'iniciou_as': data['iniciou_as'],
      'terminou_as': data['terminou_as'],
      'criado_em': datetime.now(),
      'atualizado_em': data['atualizado_em'],
      'pago_dinheiro': data['pago_dinheiro'],
      'pago_meia': data['pago_meia'],
      'gratuidade': data['gratuidade'],
      'assentos_disponiveis': data['assentos_disponiveis'],
    }
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        INSERT INTO viagem
        (id_linha, data, iniciou_as, terminou_as, criado_em, atualizado_em, pago_dinheiro, pago_meia, gratuidade, assentos_disponiveis)
        VALUES (
          {result['id_linha']},
          '{result['data']}',
          '{result['iniciou_as']}',
          '{result['terminou_as']}',
          '{result['criado_em']}',
          '{result['atualizado_em']}',
          {result['pago_dinheiro']},
          {result['pago_meia']},
          {result['gratuidade']},
          {result['assentos_disponiveis']}
          );
        ''')
    return result
  
  def get(self, id):
    with sql.connect(self.database_url) as connection:
      db = connection.cursor()
      db.execute(f'''
        SELECT * FROM viagem
        WHERE id = {id}
        ''')
      return db.fetchone()

  def update(self, id, data):
    result = {
      'id_linha': data['id_linha'],
      'data': data['data'],
      'iniciou_as': data['iniciou_as'],
      'terminou_as': data['terminou_as'],
      'criado_em': datetime.now(),
      'atualizado_em': data['atualizado_em'],
      'pago_dinheiro': data['pago_dinheiro'],
      'pago_meia': data['pago_meia'],
      'gratuidade': data['gratuidade'],
      'assentos_disponiveis': data['assentos_disponiveis'],
    }

    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        UPDATE viagem
        SET id_linha = {result["id_linha"]},
        data = '{result["data"]}',
        iniciou_as = '{result["iniciou_as"]}',
        terminou_as = '{result["terminou_as"]}',
        atualizado_em = '{result["atualizado_em"]}',
        pago_dinheiro = {result["pago_dinheiro"]},
        pago_meia = {result["pago_meia"]},
        gratuidade = {result["gratuidade"]},
        assentos_disponiveis = {result["assentos_disponiveis"]}
        WHERE id = {id};
        ''')
    return self.__dict__

  def delete(self, id):
    with sql.connect(self.database_url) as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        DELETE FROM parada
        WHERE id = {id};
        
        DELETE FROM reserva
        WHERE id_viagem = {id};

        DELETE FROM viagem
        WHERE id = {id}
        ''')
    return self.__dict__

  def get_all(self):
    with self.connection as connection:
      cursor = connection.cursor()
      cursor.execute(f'''
        SELECT * FROM viagem
        ''')
      return cursor.fetchall().__dict__
