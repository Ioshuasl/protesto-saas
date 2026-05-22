/**
 * Interface gerada para a tabela P_PESSOA
 */
export interface PPessoaInterface {
  pessoa_id: number;
  rg?: string;
  agencia?: string;
  conta?: string;
  nome_banco?: string;
  nacionalidade?: string;
  estado_civil_id?: number;
  profissao_id?: number;
  cidade_agencia?: string;
  cidade_id?: number;
  data_nascimento?: Date;
  data_validade?: Date;
  endereco?: string;
  nome?: string;
  bairro?: string;
  cidade?: string;
  observacoes?: string;
  email?: string;
  cpfcnpj?: string;
  /** Inferido na API pelo documento: F (CPF) ou J (CNPJ). */
  tipo_pessoa?: 'F' | 'J';
  uf?: string;
  cep?: string;
  telefone?: string;
  banco?: string;
  micro_empresa?: string;
  cod_cra?: string;
  nome_fantasia?: string;
  /** Quantidade de títulos distintos em que a pessoa participou (index). */
  total_titulos?: number;
}
