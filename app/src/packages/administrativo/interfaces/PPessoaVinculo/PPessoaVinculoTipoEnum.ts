/**
 * Tipos de vínculo permitidos em P_PESSOA_VINCULO (espelho de `TIPO_VINCULO_CODIGOS` na API).
 */
export const PPessoaVinculoTipoEnum = {
  APRESENTANTE: "APRESENTANTE",
  CEDENTE: "CEDENTE",
  CREDOR: "CREDOR",
  DEVEDOR: "DEVEDOR",
} as const;

export type PPessoaVinculoTipo =
  (typeof PPessoaVinculoTipoEnum)[keyof typeof PPessoaVinculoTipoEnum];

export const PPessoaVinculoTipoValues = Object.values(
  PPessoaVinculoTipoEnum,
) as PPessoaVinculoTipo[];

export const PPessoaVinculoTipoLabels: Record<PPessoaVinculoTipo, string> = {
  [PPessoaVinculoTipoEnum.APRESENTANTE]: "Apresentante",
  [PPessoaVinculoTipoEnum.CEDENTE]: "Cedente",
  [PPessoaVinculoTipoEnum.CREDOR]: "Credor",
  [PPessoaVinculoTipoEnum.DEVEDOR]: "Devedor",
};

/** Códigos legados de uma letra (ex.: mock / formulário antigo). */
const LEGACY_TIPO_VINCULO_MAP: Record<string, PPessoaVinculoTipo> = {
  A: PPessoaVinculoTipoEnum.APRESENTANTE,
  C: PPessoaVinculoTipoEnum.CEDENTE,
  R: PPessoaVinculoTipoEnum.CREDOR,
  D: PPessoaVinculoTipoEnum.DEVEDOR,
};

export function isPPessoaVinculoTipo(value: string): value is PPessoaVinculoTipo {
  return (PPessoaVinculoTipoValues as string[]).includes(value);
}

/** Normaliza para o código da API (`APRESENTANTE`, `CEDENTE`, …). */
export function normalizePPessoaVinculoTipo(
  value?: string | null,
): PPessoaVinculoTipo | undefined {
  const normalized = String(value ?? "").trim().toUpperCase();
  if (!normalized) return undefined;
  if (isPPessoaVinculoTipo(normalized)) return normalized;
  return LEGACY_TIPO_VINCULO_MAP[normalized];
}

export function formatPPessoaVinculoTipoLabel(value?: string | null): string {
  const tipo = normalizePPessoaVinculoTipo(value);
  if (!tipo) return value?.trim() || "-";
  return PPessoaVinculoTipoLabels[tipo];
}

export function pessoaVinculoTipoSearchValue(tipo: PPessoaVinculoTipo): string {
  const label = PPessoaVinculoTipoLabels[tipo];
  return [label, tipo].filter(Boolean).join(" ");
}
