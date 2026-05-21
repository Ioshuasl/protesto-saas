import type { SituacaoKey } from '@/shared/enums/SituacoesEnum';

/** Normaliza valor legado (Ativo/Inativo) ou API (A/I) para chave do enum. */
export function normalizeSituacaoKey(value?: string | null): SituacaoKey {
  const raw = (value ?? '').trim();
  if (raw === 'A' || raw.toLowerCase() === 'ativo') return 'A';
  return 'I';
}
