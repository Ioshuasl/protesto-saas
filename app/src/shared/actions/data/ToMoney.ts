// Helper: garante número com 2 casas decimais
export const toMoney = (v: unknown): number => {
  const n = Number(v ?? 0);
  // evita problemas de ponto flutuante
  return Math.round((n + Number.EPSILON) * 100) / 100;
};
