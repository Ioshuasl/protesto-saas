/** Shape enxuto retornado pelo GET index de p_titulo (API). */
export type PTituloIndexNestedEspecie = {
  especie_id?: number;
  /** Sigla FEBRABAN/CRA (coluna P_ESPECIE.ESPECIE). */
  especie?: string;
  descricao?: string;
};

export type PTituloIndexNestedOcorrencia = {
  ocorrencias_id?: number;
  descricao?: string;
};

export type PTituloIndexNestedBanco = {
  banco_id?: number;
  descricao?: string;
};

export type PTituloIndexItem = {
  titulo_id: number;
  numero_titulo?: string;
  nosso_numero?: string;
  numero_apontamento?: number;
  especie_id?: number;
  especie?: PTituloIndexNestedEspecie | null;
  valor_titulo?: number;
  ocorrencia_id?: number;
  ocorrencia?: PTituloIndexNestedOcorrencia | null;
  banco_id?: number;
  banco?: PTituloIndexNestedBanco | null;
  quantidade_pessoas_vinculadas?: number;
  apresentante_nome?: string;
  apresentante_cpfcnpj?: string;
};
