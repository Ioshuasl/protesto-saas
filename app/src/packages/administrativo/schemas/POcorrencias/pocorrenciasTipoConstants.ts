/** Valores aceitos na gravação (api/p_ocorrencias_schema.py). */
export const POCORRENCIAS_TIPO_OPCOES = [
  'CADASTRO',
  'APONTADO',
  'INTIMACAO',
  'ACEITE',
  'DESISTENCIA',
  'PAGAMENTO',
  'CANCELAMENTO',
] as const;

export type POcorrenciasTipoOpcao = (typeof POCORRENCIAS_TIPO_OPCOES)[number];

export const POCORRENCIAS_TIPO_LABELS: Record<POcorrenciasTipoOpcao, string> = {
  CADASTRO: 'Cadastro',
  APONTADO: 'Apontado',
  INTIMACAO: 'Intimação',
  ACEITE: 'Aceite',
  DESISTENCIA: 'Desistência',
  PAGAMENTO: 'Pagamento',
  CANCELAMENTO: 'Cancelamento',
};
