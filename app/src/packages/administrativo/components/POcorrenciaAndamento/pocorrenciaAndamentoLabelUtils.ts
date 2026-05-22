import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';

export function ocorrenciaAndamentoLabel(
  item: Pick<POcorrenciaAndamentoInterface, 'ocorrencia_andamento_id' | 'codigo' | 'descricao'>,
): string {
  const codigo = item.codigo?.trim().toUpperCase();
  const descricao = item.descricao?.trim();
  if (codigo && descricao) return `${codigo} — ${descricao}`;
  return descricao || codigo || `Ocorrência ${item.ocorrencia_andamento_id}`;
}

/** Texto usado na busca do combobox (código + descrição). */
export function ocorrenciaAndamentoSearchValue(
  item: Pick<
    POcorrenciaAndamentoInterface,
    'ocorrencia_andamento_id' | 'codigo' | 'descricao'
  >,
): string {
  const codigo = String(item.codigo ?? '').trim();
  const descricao = String(item.descricao ?? '').trim();
  return [codigo, descricao, ocorrenciaAndamentoLabel(item)].filter(Boolean).join(' ');
}
