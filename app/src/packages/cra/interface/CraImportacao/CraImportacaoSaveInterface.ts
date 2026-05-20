import type { CraRemessaParsed } from "@/packages/cra/functions/CraImportacao";

export interface CraImportacaoSavePayload {
  banco_id: number;
  remessa: CraRemessaParsed;
}

export interface CraImportacaoSaveResult {
  importacao_id: string;
  banco_id: number;
  file_name: string;
  imported_count: number;
  titulo_ids: number[];
  nosso_numeros: string[];
}

export function isCraImportacaoSaveResult(value: unknown): value is CraImportacaoSaveResult {
  if (!value || typeof value !== "object") return false;
  const parsed = value as Partial<CraImportacaoSaveResult>;
  return (
    typeof parsed.importacao_id === "string" &&
    typeof parsed.banco_id === "number" &&
    typeof parsed.file_name === "string" &&
    typeof parsed.imported_count === "number" &&
    Array.isArray(parsed.titulo_ids)
  );
}
