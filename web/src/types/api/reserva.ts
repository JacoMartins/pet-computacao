export interface reserva {
  id: number;
  id_viagem: number;
  id_usuario: number;
  assento: number;
  forma_pagamento: string;
  criado_em: string;
  atualizado_em: string;
}

export interface response_reserva {
  status: number;
  message: string;
  data: reserva[];
}