import type { PTituloSeloVinculadoItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem';

function parseSeloDate(value: string | Date | undefined): number {
  if (value == null || value === '') return Number.NaN;
  if (value instanceof Date) return value.getTime();
  const s = String(value).trim();
  const mBr = s.match(/^(\d{2})\.(\d{2})\.(\d{4})(?:\s+(\d{2}):(\d{2}))?/);
  if (mBr) {
    const [, d, mo, y, h, min] = mBr;
    return new Date(
      Number(y),
      Number(mo) - 1,
      Number(d),
      h != null ? Number(h) : 0,
      min != null ? Number(min) : 0,
    ).getTime();
  }
  return new Date(s).getTime();
}

/** Ordem cronológica (apontamento → intimação → protesto). */
export function sortPTituloSelosVinculados(
  items: PTituloSeloVinculadoItem[],
): PTituloSeloVinculadoItem[] {
  return [...items].sort((a, b) => {
    const ta = parseSeloDate(a.data ?? a.data_hora_utilizacao);
    const tb = parseSeloDate(b.data ?? b.data_hora_utilizacao);
    if (!Number.isNaN(ta) && !Number.isNaN(tb) && ta !== tb) return ta - tb;
    return (a.selo_livro_id ?? 0) - (b.selo_livro_id ?? 0);
  });
}
