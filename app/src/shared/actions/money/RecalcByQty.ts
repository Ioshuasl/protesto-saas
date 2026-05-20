type MoneyValue = number | null | undefined;

type RecalcConfig<T> = {
  qtyKey: keyof T; // ex: 'qtd'
  fields: (keyof T)[]; // ex: ['emolumento','taxa_judiciaria',...]
  decimals?: number; // default 2
  minQty?: number; // default 1
};

export class RecalcByQty {
  static asNumber(v: unknown): number | null {
    if (v === null || v === undefined) return null;
    const n = typeof v === 'number' ? v : Number(v);
    return Number.isFinite(n) ? n : null;
  }

  static round(n: number, decimals = 2): number {
    const p = 10 ** decimals;
    return Math.round((n + Number.EPSILON) * p) / p;
  }

  /**
   * Recalcula campos de valores (totais) proporcionalmente à nova quantidade.
   * Pressuposto: os valores em `fields` são TOTAIS para a qtd original do item.
   */
  static recalc<T extends Record<string, any>>(item: T, nextQty: number, cfg: RecalcConfig<T>): T {
    const decimals = cfg.decimals ?? 2;
    const minQty = cfg.minQty ?? 1;

    const originalQtyRaw = this.asNumber(item[cfg.qtyKey]);
    const originalQty = Math.max(minQty, originalQtyRaw ?? minQty);
    const qty = Math.max(0, Number.isFinite(nextQty) ? nextQty : 0);

    const out: T = { ...item, [cfg.qtyKey]: qty } as T;

    for (const field of cfg.fields) {
      const raw = item[field] as MoneyValue;

      // mantém null/undefined como está
      if (raw === null || raw === undefined) {
        out[field] = raw as any;
        continue;
      }

      const total = this.asNumber(raw);
      if (total === null) {
        out[field] = raw as any;
        continue;
      }

      const unit = total / originalQty;
      const nextTotal = unit * qty;
      out[field] = this.round(nextTotal, decimals) as any;
    }

    return out;
  }

  /**
   * Helper para detectar se mudou (com arredondamento).
   */
  static isDirty<T extends Record<string, any>>(
    original: T,
    recalced: T,
    cfg: RecalcConfig<T>,
  ): boolean {
    const decimals = cfg.decimals ?? 2;

    const oq = this.asNumber(original[cfg.qtyKey]);
    const nq = this.asNumber(recalced[cfg.qtyKey]);
    if ((oq ?? 0) !== (nq ?? 0)) return true;

    for (const field of cfg.fields) {
      const o = original[field];
      const n = recalced[field];

      if (o === null || o === undefined) continue;

      const on = this.asNumber(o);
      const nn = this.asNumber(n);

      if (on === null || nn === null) continue;

      if (this.round(on, decimals) !== this.round(nn, decimals)) return true;
    }

    return false;
  }
}
