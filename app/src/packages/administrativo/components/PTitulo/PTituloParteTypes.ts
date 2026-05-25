"use client";

import {
  PPessoaVinculoTipoEnum,
  formatPPessoaVinculoTipoLabel,
  normalizePPessoaVinculoTipo,
  type PPessoaVinculoTipo,
} from "@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoTipoEnum";

export interface PTituloParteItem {
  pessoa_id?: number;
  tipo: string;
  descricao: string;
  nome?: string;
  cpfcnpj?: string;
  devedor_microempresa?: unknown;
  micro_empresa?: unknown;
}

export const PTITULO_PARTE_DEFAULT_TIPO = PPessoaVinculoTipoEnum.DEVEDOR;

export function parteTipoDescricao(tipo?: string | null): string {
  return formatPPessoaVinculoTipoLabel(tipo);
}

export function buildPTituloParteItem(
  partial: Omit<PTituloParteItem, "tipo" | "descricao"> & {
    tipo?: string | null;
    descricao?: string;
  },
): PTituloParteItem {
  const tipo = normalizePPessoaVinculoTipo(partial.tipo) ?? PTITULO_PARTE_DEFAULT_TIPO;
  return {
    ...partial,
    tipo,
    descricao: partial.descricao?.trim() || parteTipoDescricao(tipo),
  };
}

export type { PPessoaVinculoTipo };
