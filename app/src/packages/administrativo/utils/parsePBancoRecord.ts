import type { PBancoInterface } from "@/packages/administrativo/interfaces/PBanco/PBancoInterface";

function toFiniteNumber(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim() !== "") {
    const parsed = Number(value);
    if (Number.isFinite(parsed)) return parsed;
  }
  return null;
}

function extractBancoCandidate(value: Record<string, unknown>): Record<string, unknown> | null {
  if ("banco_id" in value || "codigo_banco" in value) {
    return value;
  }

  const nested = value.data;
  if (nested && typeof nested === "object" && !Array.isArray(nested)) {
    const record = nested as Record<string, unknown>;
    if ("banco_id" in record || "codigo_banco" in record) {
      return record;
    }
  }

  return null;
}

/** Normaliza resposta da API / server action para `PBancoInterface`. */
export function parsePBancoRecord(value: unknown): PBancoInterface | null {
  if (value == null || typeof value !== "object") return null;

  const root = value as Record<string, unknown>;
  if (typeof root.status === "number" && root.status >= 600) return null;

  const candidate = extractBancoCandidate(root);
  if (!candidate) return null;

  const bancoId = toFiniteNumber(candidate.banco_id);
  if (bancoId == null) return null;

  return {
    ...(candidate as Omit<PBancoInterface, "banco_id">),
    banco_id: bancoId,
  } as PBancoInterface;
}
