export type PTituloIndexQuery = {
  /** Busca unificada por pessoa, CPF/CNPJ, protocolo, nosso número e número do título. */
  busca?: string;
  /** Busca em P_PESSOA_VINCULO (nome/cpfcnpj) e P_PESSOA vinculada. */
  busca_pessoa?: string;
  numero_apontamento?: number;
  nosso_numero?: string;
  numero_titulo?: string;
  numero_titulo_banco?: string;
  ocorrencia_id?: number;
  ocorrencia_andamento_id?: number;
  banco_id?: number;
  especie_id?: number;
  situacao_data?:
    | "somente_cadastro"
    | "somente_apontado"
    | "somente_intimado"
    | "somente_protestado";
  workflow_etapa?: "apontamento" | "intimacao" | "protesto";
  workflow_status?: "pendente" | "concluido";
  /** Página da API (query `p`). */
  page?: number;
  per_page?: number;
  /** formato3: ex. titulo_id.desc */
  sort?: string;
};
