import sqlite3
import os
from utils.response_message import response_message
from utils.type import typeString, sqlType, sqlDataType

class create_schema:
    def __init__(self, **kwargs):
      self.table_name = kwargs.get('table_name')
      self.fields = kwargs.get('fields')
      self.dependants = kwargs.get('dependants')

      self.database_url = kwargs.get('database_url')

    def validate(self, **kwargs):
      fields = self.fields

      for key, value in kwargs.items():
        if key not in fields:
          raise Exception(f'Key {key} not in schema')

        if type(value) != fields[key][0]:
          raise Exception(f'Value {value} is not {typeString(fields[key][0])}.')

    def validate_field(self, key):
      fields = self.fields

      if key not in fields:
        raise Exception(f'Key {key} not in schema')

    def create_dict(self, args:list):
      fields = self.fields

      dict = {}
      
      for i in range(len(args)):
        dict[list(fields.keys())[i]] = args[i]

      self.validate(**dict)
        
      return dict

    def create_table(self):
      fields = self.fields

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'CREATE TABLE IF NOT EXISTS {self.table_name} ('
        for key, keyTypes in fields.items():
          if key.startswith('FK') or key.startswith('fk'):
            sql += f'FOREIGN KEY ({keyTypes[0]}) REFERENCES {keyTypes[1]}'
          elif key.startswith('PK') or key.startswith('pk'):
            sql += f'PRIMARY KEY ({keyTypes[0]})'
          else:
            for keyType in keyTypes:
              if keyTypes.index(keyType) == 0:
                sql += f'{key} {sqlType(keyType)}'
              else:
                sql += f' {keyType}'
          
          sql += ', '

        sql = sql[:-2] + ');'

        cursor.execute(sql)
      return response_message(status=200, message=f'Tabela {self.table_name} criada com sucesso.').get_dict()

    # INSERT
    
    def insert(self, **kwargs):
      fields = self.fields

      self.validate(**kwargs)

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'INSERT INTO {self.table_name} ('
        for key, keyTypes in fields.items():
          try: autoincrement = keyTypes.index('AUTOINCREMENT')
          except: autoincrement = False  

          if not autoincrement:
              sql += f'{key}, '

        sql = sql[:-2] + ') VALUES ('

        for key, keyTypes in fields.items():
          try: autoincrement = keyTypes.index('AUTOINCREMENT')
          except: autoincrement = False

          if not autoincrement:
              sql += '?, '
            
        sql = sql[:-2] + ');'

        cursor.execute(sql, tuple(kwargs.values()))

      return response_message(status=200, message=f'Objeto inserido com sucesso.', data=self.get_last()['data']).get_dict()

    # SELECT

    def select_all(self):
      fields = self.fields

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'SELECT * FROM {self.table_name};'

        cursor.execute(sql)

        return cursor.fetchall()

    def select_last(self):
      fields = self.fields

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT 1;'

        cursor.execute(sql)

        return cursor.fetchone()

    def select_one(self, **kwargs):
      fields = self.fields
      where = kwargs.get('where')

      self.validate_field(where['field'])

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'SELECT * FROM {self.table_name} WHERE '

        for key, keyTypes in fields.items():
          if key == where['field']:
            sql += f'{key} {where["operator"]} {sqlDataType(where["value"])}, '

        sql = sql[:-2] + ';'

        cursor.execute(sql)

        return cursor.fetchone()

    def select_many(self, **kwargs):
      fields = self.fields
      where = kwargs.get('where')

      self.validate_field(where['field'])

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'SELECT * FROM {self.table_name} WHERE '

        for key, keyTypes in fields.items():
          if key == where['field']:
            sql += f'{key} {where["operator"]} {sqlDataType(where["value"])}, '

        sql = sql[:-2] + ';'

        cursor.execute(sql)

        return cursor.fetchall()

    # UPDATE

    def update_one(self, **kwargs):
      fields = self.fields
      where = kwargs.get('where')
      data = kwargs.get('data')

      dataExists = self.select_one(where=where)

      if dataExists == None:
        return response_message(status=404, message=f'Erro ao atualizar: Nenhum objeto contendo o valor {sqlDataType(where["value"])} no campo {sqlDataType(where["field"])} foi encontrado.').get_dict()

      self.validate(**data)

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'UPDATE {self.table_name} SET '

        for key, value in data.items():
          sql += f'{key} = {sqlDataType(value)}, '

        sql = sql[:-2] + ' WHERE '

        for key, keyTypes in fields.items():
          if key == where['field']:
            sql += f'{key} {where["operator"]} {sqlDataType(where["value"])}, '

        sql = sql[:-2] + ';'

        cursor.execute(sql)

      return response_message(status=200, message=f'Objeto atualizado com sucesso.').get_dict()

    def update_many(self, **kwargs):
      fields = self.fields
      where = kwargs.get('where')
      data = kwargs.get('data')

      dataExists = self.select_many(where=where)

      if len(dataExists) == 0:
        return response_message(status=404, message=f'Erro ao atualizar: Nenhum objeto contendo o valor {sqlDataType(where["value"])} no campo {sqlDataType(where["field"])} foi encontrado.').get_dict()

      self.validate(**data)

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'UPDATE {self.table_name} SET '

        for key, value in data.items():
          sql += f'{key} = {sqlDataType(value)}, '

        sql = sql[:-2] + ' WHERE '

        for key, keyTypes in fields.items():
          if key == where['field']:
            sql += f'{key} {where["operator"]} {sqlDataType(where["value"])}, '

        sql = sql[:-2] + ';'

        cursor.execute(sql)

      return response_message(status=200, message=f'{len(dataExists)} objetos contendo o valor {sqlDataType(where["value"])} no campo {sqlDataType(where["field"])} foram atualizados.').get_dict()

    # DELETE

    def delete_many(self, **kwargs):
      fields = self.fields
      where = kwargs.get('where')

      dataExists = self.select_many(where=where)

      if len(dataExists) == 0:
        return response_message(status=404, message=f'Erro ao deletar: Nenhum objeto contendo o valor {sqlDataType(where["value"])} no campo {sqlDataType(where["field"])} foi encontrado.').get_dict()

      self.validate_field(where['field'])

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'DELETE FROM {self.table_name} WHERE '

        for key, keyTypes in fields.items():
          if key == where['field']:
            sql += f'{key} {where["operator"]} {sqlDataType(where["value"])}, '

        sql = sql[:-2] + ';'

        cursor.execute(sql)
      return response_message(status=200, message=f'{len(dataExists)} objetos contendo o valor {sqlDataType(where["value"])} no campo {sqlDataType(where["field"])} deletado com sucesso.').get_dict()

    def delete_all(self):
      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'DELETE * FROM {self.table_name};'

        cursor.execute(sql)
      return response_message(status=200, message='Todos os objetos foram deletados com sucesso.').get_dict()

    def delete_one(self, **kwargs):
      fields = self.fields
      where = kwargs.get('where')

      dataExists = self.select_one(where=where)

      if dataExists == None:
        return response_message(status=404, message=f'Erro ao deletar: Nenhum objeto contendo o valor {sqlDataType(where["value"])} no campo {sqlDataType(where["field"])} foi encontrado.').get_dict()

      self.validate_field(where['field'])

      with sqlite3.connect(self.database_url) as connection:
        cursor = connection.cursor()

        sql = f'DELETE FROM {self.table_name} WHERE '

        for key, keyTypes in fields.items():
          if key == where['field']:
            sql += f'{key} {where["operator"]} {sqlDataType(where["value"])}, '

        sql = sql[:-2] + ';'

        cursor.execute(sql)
      return response_message(status=200, message=f'1 objeto contendo o valor {sqlDataType(where["value"])} no campo {sqlDataType(where["field"])} foi deletado com sucesso.').get_dict()

    # GET

    def get_all(self):
      result = [self.create_dict(row) for row in self.select_all()]
      
      if len(result) == 0:
        return response_message(status=200, message='Nada encontrado.', data=result).get_dict()
      elif result == None:
        return response_message(status=500, message='Erro interno do servidor.').get_dict()
      
      return response_message(status=200, message=f'{len(result)} objetos encontrados com sucesso.', data=result).get_dict()

    def get_one(self, **kwargs):
      data = self.select_one(**kwargs)

      if data == None:
        return response_message(status=404, message='Não encontrado.').get_dict()

      result = self.create_dict(data)

      return response_message(status=200, message='1 objeto foi encontrado com sucesso.', data=result).get_dict()
    
    def get_last(self):
      data = self.select_last()

      if data == None:
        return response_message(status=404, message='Não encontrado.').get_dict()

      result = self.create_dict(data)

      return response_message(status=200, message='1 objeto foi encontrado com sucesso.', data=result).get_dict()

    def get_many(self, **kwargs):
      result = [self.create_dict(row) for row in self.select_many(**kwargs)]

      if len(result) == 0:
        return response_message(status=200, message='Nada encontrado.', data=result).get_dict()
      elif result == None:
        return response_message(status=500, message='Erro interno do servidor.').get_dict()
      
      return response_message(status=200, message=f'{len(result)} objetos encontrados com sucesso.', data=result).get_dict()

class simple:
  def __init__(self, **kwargs):
    self.database_url = kwargs.get('database_url')
    self.schemas = kwargs.get('schemas')

    self.dependants = []

    for schema in self.schemas:
      setattr(self, schema['name'], create_schema(database_url=self.database_url, table_name=schema['name'], fields=schema['fields'], dependants=self.dependants))
      
      self.dependants.append({
        'table': schema['name'],
        'depends_on': []
      })

      for key, value in schema['fields'].items():
        if key.startswith('fk') or key.startswith('FK'):
          self.dependants[-1]['depends_on'].append({
            'table': value[1].split('(')[0],
            'field': value[0],
          })

  def setup(self):
    if not os.path.exists(self.database_url):
      open(self.database_url, 'a').close()

    for schema in self.schemas:
      self.__getattribute__(schema['name']).create_table()