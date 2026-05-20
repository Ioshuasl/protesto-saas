/**
 * Interface gerada para a tabela P_PESSOA_VINCULO
 */
export interface PPessoaVinculoInterface {
  pessoa_vinculo_id: number;
  rg?: string;
  titulo_id?: number;
  pessoa_id?: number;
  agencia?: string;
  conta?: string;
  nome_banco?: string;
  nacionalidade?: string;
  estado_civil_id?: number;
  profissao_id?: number;
  cidade_agencia?: string;
  devedor_data_aceite?: Date;
  ocorrencia_id?: number;
  endereco?: string;
  devedor_agencia?: string;
  devedor_numero_ar?: string;
  devedor_recebido_por?: string;
  devedor_situacao?: string;
  nome?: string;
  bairro?: string;
  cidade?: string;
  cpfcnpj?: string;
  uf?: string;
  cep?: string;
  telefone?: string;
  tipo_vinculo?: string;
  banco?: string;
  principal?: string;
  favorecido?: string;
  gerar_selo?: string;
  devedor_tipo_aceite?: string;
  devedor_microempresa?: string;
  ocorrencia_andamento_id?: number;
  controle_devedor?: number;
}
