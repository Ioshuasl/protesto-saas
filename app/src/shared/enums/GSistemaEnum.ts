export const GSistemaEnum = {
  '1': { sistema_id: 2, descricao: 'Tabelionato de Notas', situacao: 'A', tipo_cartorio: '1' },
  '2': { sistema_id: 1, descricao: 'Registro de Imóveis', situacao: 'A', tipo_cartorio: '2' },
  '3': { sistema_id: 12, descricao: 'Registro Civil', situacao: 'A', tipo_cartorio: '3' },
  '4': { sistema_id: 7, descricao: 'RTD', situacao: 'A', tipo_cartorio: '4' },
  '5': { sistema_id: 13, descricao: 'Tabelionato de Protesto', situacao: 'A', tipo_cartorio: '5' },
} as const;

export type GSistemaKey = keyof typeof GSistemaEnum;
