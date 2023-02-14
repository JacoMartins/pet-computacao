from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class schema_linha: 
  def __init__(self, cod, nome, distancia_km, destino, valor_dinheiro, capacidade_de_assento, id=None, criado_em=now, atualizado_em=now, valor_meia=None):
    self.id = id
    self.cod = cod
    self.nome = nome
    self.distancia_km = distancia_km
    self.criado_em = criado_em
    self.atualizado_em = atualizado_em
    self.destino = destino
    self.valor_dinheiro = valor_dinheiro
    self.valor_meia = valor_meia if valor_meia else valor_dinheiro / 2
    self.capacidade_de_assento = capacidade_de_assento

  def get_dict(self):
    return self.__dict__

class schema_parada:
  def __init__(self, id_linha, hora_de_parada, parada, id=None, criado_em=now, atualizado_em=now):
    self.id = id
    self.id_linha = id_linha
    self.hora_de_parada = hora_de_parada
    self.parada = parada
    self.criado_em = criado_em
    self.atualizado_em = atualizado_em

  def get_dict(self):
    return self.__dict__

class schema_reserva:
  def __init__(self, id_viagem, assento, id=None, criado_em=now, atualizado_em=now):
    self.id = id
    self.id_viagem = id_viagem
    self.assento = assento
    self.criado_em = criado_em
    self.atualizado_em = atualizado_em
  
  def get_dict(self):
    return self.__dict__

class schema_viagem:
  def __init__(self, id_linha, data, iniciou_as, terminou_as, assentos_disponiveis, id=None, criado_em=now, atualizado_em=now, pago_dinheiro=0, pago_meia=0, gratuidade=0):
    self.id = id
    self.id_linha = id_linha
    self.data = data
    self.iniciou_as = iniciou_as
    self.terminou_as = terminou_as
    self.criado_em = criado_em
    self.atualizado_em = atualizado_em
    self.pago_dinheiro = pago_dinheiro
    self.pago_meia = pago_meia
    self.gratuidade = gratuidade
    self.assentos_disponiveis = assentos_disponiveis
  
  def get_dict(self):
    return self.__dict__