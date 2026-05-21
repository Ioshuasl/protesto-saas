import { useEffect, useMemo, useState } from 'react';

import type { PLivroAndamentoProximoNumero } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoProximoNumero';
import { PLivroAndamentoProximoNumeroService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoProximoNumeroService';

/** Cache em memória da sessão — evita refetch ao trocar natureza no mesmo formulário. */
const proximoNumeroCache = new Map<number, number>();

export function invalidateProximoNumeroCache(livroNaturezaId?: number) {
  if (livroNaturezaId != null) {
    proximoNumeroCache.delete(livroNaturezaId);
  } else {
    proximoNumeroCache.clear();
  }
}

function isProximoNumeroResult(value: unknown): value is PLivroAndamentoProximoNumero {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof (value as PLivroAndamentoProximoNumero).numero_livro_sugerido === 'number'
  );
}

function mapFromCache(ids: number[]): Record<number, number> {
  const map: Record<number, number> = {};
  for (const id of ids) {
    const sugerido = proximoNumeroCache.get(id);
    if (sugerido != null) map[id] = sugerido;
  }
  return map;
}

/**
 * Pré-carrega MAX(NUMERO_LIVRO)+1 para cada livro_natureza_id (em paralelo).
 * Retorna mapa id → numero_livro_sugerido para troca instantânea no formulário.
 */
export function useProximoNumeroPorNatureza(naturezaIds: number[], enabled: boolean) {
  const [proximoNumeroPorNatureza, setProximoNumeroPorNatureza] = useState<Record<number, number>>(
    () => (enabled ? mapFromCache(naturezaIds) : {}),
  );
  const [isLoading, setIsLoading] = useState(false);

  const idsKey = useMemo(() => naturezaIds.slice().sort((a, b) => a - b).join(','), [naturezaIds]);

  useEffect(() => {
    if (!enabled || naturezaIds.length === 0) {
      setProximoNumeroPorNatureza({});
      return;
    }

    const cached = mapFromCache(naturezaIds);
    setProximoNumeroPorNatureza(cached);

    const missing = naturezaIds.filter((id) => !proximoNumeroCache.has(id));
    if (missing.length === 0) return;

    let cancelled = false;
    setIsLoading(true);

    void Promise.all(
      missing.map(async (livroNaturezaId) => {
        const result = await PLivroAndamentoProximoNumeroService(livroNaturezaId);
        if (!isProximoNumeroResult(result)) return null;
        proximoNumeroCache.set(livroNaturezaId, result.numero_livro_sugerido);
        return { livroNaturezaId, sugerido: result.numero_livro_sugerido };
      }),
    )
      .then((results) => {
        if (cancelled) return;
        const next = mapFromCache(naturezaIds);
        for (const row of results) {
          if (row) next[row.livroNaturezaId] = row.sugerido;
        }
        setProximoNumeroPorNatureza(next);
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [enabled, idsKey, naturezaIds]);

  return { proximoNumeroPorNatureza, isLoadingProximos: isLoading };
}
