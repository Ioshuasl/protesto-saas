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

export type PTituloIndexPessoaVinculo = {
  pessoa_vinculo_id?: number;
  titulo_id?: number;
  pessoa_id?: number;
  nome?: string;
  cpfcnpj?: string;
  tipo_vinculo?: string;
  devedor_microempresa?: unknown;
  pessoa?: {
    pessoa_id?: number;
    nome?: string;
    cpfcnpj?: string;
    micro_empresa?: unknown;
  };
};

export type PTituloIndexItem = {
  titulo_id: number;
  data_intimacao?: Date | string;
  data_protesto?: Date | string;
  data_aceite?: Date | string;
  data_apontamento?: Date | string;
  data_cancelamento?: Date | string;
  data_emissao_titulo?: Date | string;
  data_cadastro?: Date | string;
  data_sustado?: Date | string;
  data_pago?: Date | string;
  livro_id_protesto?: number;
  folha_protesto?: number;
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
  pessoa_vinculos?: PTituloIndexPessoaVinculo[];
};
