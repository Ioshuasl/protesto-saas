import type { PAndamentoArquivoGeradoCodigo } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoInterface';

export const ARQUIVO_GERADO_AGUARDANDO: PAndamentoArquivoGeradoCodigo = 'D';
export const ARQUIVO_GERADO_EXPORTADO: PAndamentoArquivoGeradoCodigo = 'E';

export const ARQUIVO_GERADO_OPTIONS: {
  value: PAndamentoArquivoGeradoCodigo;
  label: string;
}[] = [
  { value: ARQUIVO_GERADO_AGUARDANDO, label: 'Aguardando' },
  { value: ARQUIVO_GERADO_EXPORTADO, label: 'Exportado' },
];

export function labelArquivoGerado(
  codigo?: PAndamentoArquivoGeradoCodigo | string | null,
): string {
  if (!codigo) return '—';
  const normalized = String(codigo).trim().toUpperCase();
  const found = ARQUIVO_GERADO_OPTIONS.find((o) => o.value === normalized);
  return found?.label ?? normalized;
}
