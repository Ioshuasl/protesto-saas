const ptituloMoneyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

export function parsePTituloMoneyValue(value: unknown): number {
  const raw = String(value ?? "").replace(/[^\d.,-]/g, "");
  const hasComma = raw.includes(",");
  const hasDot = raw.includes(".");
  const normalized =
    hasComma && hasDot
      ? raw.lastIndexOf(",") > raw.lastIndexOf(".")
        ? raw.replace(/\./g, "").replace(",", ".")
        : raw.replace(/,/g, "")
      : hasComma
        ? raw.replace(",", ".")
        : raw;

  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : 0;
}

export function formatPTituloMoneyValue(value: unknown): string {
  return ptituloMoneyFormatter.format(parsePTituloMoneyValue(value));
}
