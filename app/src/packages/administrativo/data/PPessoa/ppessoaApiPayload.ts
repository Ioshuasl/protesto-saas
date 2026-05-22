import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';

const API_FIELDS = [
  'nome',
  'tipo_pessoa',
  'cpfcnpj',
  'endereco',
  'bairro',
  'cidade',
  'uf',
  'cep',
  'telefone',
  'rg',
  'observacoes',
  'banco',
  'agencia',
  'conta',
  'nome_banco',
  'nacionalidade',
  'estado_civil_id',
  'profissao_id',
  'cidade_agencia',
  'data_nascimento',
  'email',
  'cidade_id',
  'data_validade',
  'micro_empresa',
  'chave_pessoa_imp',
  'cod_cra',
  'nome_fantasia',
] as const;

export function toPPessoaApiPayload(
  data: Partial<PPessoaInterface>,
): Record<string, unknown> {
  const payload: Record<string, unknown> = {};

  for (const key of API_FIELDS) {
    if (key in data && data[key] !== undefined) {
      payload[key] = data[key];
    }
  }

  return payload;
}
