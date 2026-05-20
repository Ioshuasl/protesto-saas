export interface PTituloProtestarBatchInterface {
  titulo_id: number;
  numero_titulo?: string;
  nosso_numero?: string;
  numero_apontamento?: number;
  data_apontamento?: Date;
  data_intimacao?: Date;
  data_protesto?: Date;
  data_cadastro?: Date;
  valor_titulo?: number;
  banco_id?: number;
  apresentante?: string;
  cpfcnpj?: string;
  situacao_aceite?: string;
}
