"use client";

import db from "@/db.json";
import type { PTituloStatusImportacao, PTituloTipoEndosso } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import type { PTituloSelectOption } from "./PTituloDetailsFormSchema";

export type { PTituloSelectOption };

export const emolumentoItemOptions: PTituloSelectOption[] =
  (db as { emolumentos?: Array<{ emolumento_id: number; descricao?: string }> }).emolumentos?.map(
    (item) => ({
      value: String(item.emolumento_id),
      label: item.descricao ?? "-",
    }),
  ) ?? [];

export const tipoEndossoOptions: PTituloSelectOption<PTituloTipoEndosso>[] = [
  { value: "M", label: "Mandato" },
  { value: "T", label: "Translativo" },
];

export const formaPagamentoOptions: PTituloSelectOption[] = [
  { value: "Boleto", label: "Boleto" },
  { value: "PIX", label: "PIX" },
  { value: "Dinheiro", label: "Dinheiro" },
  { value: "Transferência", label: "Transferência" },
];

export const statusImportacaoOptions: PTituloSelectOption<PTituloStatusImportacao>[] = [
  { value: "D", label: "Aguardando" },
  { value: "E", label: "Exportado" },
];

export const situacaoAceiteOptions: PTituloSelectOption[] = [
  { value: "Pendente", label: "Pendente" },
  { value: "Aceito", label: "Aceito" },
  { value: "Recusado", label: "Recusado" },
];

export { tituloTipoAceiteSelectOptions as tipoAceiteOptions, tituloBooleanSelectOptions as booleanOptions } from "./PTituloDetailsFormSchema";
