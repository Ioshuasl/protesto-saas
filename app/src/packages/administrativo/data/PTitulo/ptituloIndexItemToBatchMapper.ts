import type { PTituloIndexItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexItem';

/** Campos comuns às telas de lote (apontamento, intimação, protesto). */
export type PTituloBatchRowBase = {
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
};

function parseDate(value: Date | string | undefined): Date | undefined {
  if (!value) return undefined;
  if (value instanceof Date) return value;
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? undefined : parsed;
}

export function mapPTituloIndexItemToBatchRow(item: PTituloIndexItem): PTituloBatchRowBase {
  return {
    titulo_id: item.titulo_id,
    numero_titulo: item.numero_titulo,
    nosso_numero: item.nosso_numero,
    numero_apontamento: item.numero_apontamento,
    data_apontamento: parseDate(item.data_apontamento),
    data_intimacao: parseDate(item.data_intimacao),
    data_protesto: parseDate(item.data_protesto),
    data_cadastro: parseDate(item.data_cadastro),
    valor_titulo: item.valor_titulo,
    banco_id: item.banco_id,
    apresentante: item.apresentante_nome,
    cpfcnpj: item.apresentante_cpfcnpj,
  };
}
