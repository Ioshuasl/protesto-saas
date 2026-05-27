export interface GSistemaInterface {
  sistema_id: number;
  descricao?: string;
  situacao?: string;
  tipo_cartorio?: string;
  versao?: string;
  data_versao?: Date | string;
  nome_exe?: string;
}
