import type { PTituloInterface } from "./PTituloInterface";
import type { PTituloSeloVinculadoItem } from "./PTituloSeloVinculadoItem";

export type TituloStatus =
  | "Apontado"
  | "Em Tríduo"
  | "Liquidado"
  | "Pago"
  | "Protestado"
  | "Desistido"
  | "Cancelado";

/** Resposta de service com `withClientErrorHandler` vs linha enriquecida de título. */
export function isTituloListItem(value: unknown): value is TituloListItem {
  if (typeof value !== "object" || value === null) return false;
  if (!("titulo_id" in value)) return false;
  const row = value as { vinculos_partes?: unknown };
  return Array.isArray(row.vinculos_partes);
}

/** Linha enriquecida para listagem/detalhe de título (camada de apresentação). */
export interface TituloListItem extends PTituloInterface {
  devedor_nome?: string;
  devedor_cpfcnpj?: string;
  especie_sigla?: string;
  status_descricao?: string;
  apresentante_nome?: string;
  apresentante_cpfcnpj?: string;
  credor_nome?: string;
  cedente_nome?: string;
  partes_label?: string;
  partes_documentos?: string;
  vinculos_partes: Array<{
    pessoa_vinculo_id?: number;
    tipo: string;
    descricao: string;
    devedor_tipo_aceite?: string;
    devedor_data_aceite?: Date;
    nome?: string;
    cpfcnpj?: string;
  }>;
  vinculos_selos?: PTituloSeloVinculadoItem[];
}
