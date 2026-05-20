import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";

export interface PCertidaoConsultaApresentantePayload {
  apresentante: string;
  cpfcnpj: string;
  data_inicio?: string;
  data_fim?: string;
}

export interface PCertidaoConsultaApresentanteResult {
  titulosPorDocumento: TituloListItem[];
  candidatosHomonimia: TituloListItem[];
}

export function isPCertidaoConsultaApresentanteResult(
  value: unknown,
): value is PCertidaoConsultaApresentanteResult {
  if (!value || typeof value !== "object") return false;
  const candidate = value as { titulosPorDocumento?: unknown; candidatosHomonimia?: unknown };
  return Array.isArray(candidate.titulosPorDocumento) && Array.isArray(candidate.candidatosHomonimia);
}
