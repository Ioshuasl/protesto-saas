"use client";

import type {
  PTituloTipoAceite,
  PTituloTipoEndosso,
} from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import type {
  PTituloDetailsFormValues,
  PTituloDetailsScalarKey,
  PTituloSelectOption,
  PTituloSelectOptionsByField,
} from "./PTituloDetailsFormSchema";
import { pTituloDetailsScalarKeys } from "./PTituloDetailsFormSchema";

/** Opções vindas de hooks/API (`selectOptionsByField`) substituem as estáticas do `db.json` para o mesmo campo. */
export function mergeTituloSelectOptions(
  name: PTituloDetailsScalarKey,
  staticOptions: PTituloSelectOption[],
  selectOptionsByField?: PTituloSelectOptionsByField,
): PTituloSelectOption[] {
  return selectOptionsByField?.[name] ?? staticOptions;
}

function formatDateValue(value: Date | string | undefined): string {
  if (!value) return "";
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return "";

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatMoneyValue(value?: number): string {
  if (!value && value !== 0) return "";
  return value.toFixed(2);
}

export function parsePTituloIsoDate(value?: string): Date | undefined {
  if (!value) return undefined;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? undefined : date;
}

export function sanitizePTituloPositiveNumber(rawValue: string, allowDecimal: boolean): string {
  const cleaned = rawValue.replace(/[^\d.,]/g, "").replace(",", ".");
  if (!allowDecimal) return cleaned.replace(/\./g, "");

  const [integerPart = "", ...fractionParts] = cleaned.split(".");
  const fraction = fractionParts.join("");
  return fraction ? `${integerPart}.${fraction}` : integerPart;
}

function normalizePTituloTipoAceite(value: unknown): PTituloTipoAceite | "" {
  if (value === "A" || value === "Aceite") return "A";
  if (value === "E" || value === "Edital") return "E";
  return "";
}

function normalizePTituloTipoEndosso(value: unknown): PTituloTipoEndosso | "" {
  if (value === "M" || value === "Mandato") return "M";
  if (value === "T" || value === "Translativo") return "T";
  return "";
}

function isDateScalarKey(key: PTituloDetailsScalarKey): boolean {
  return key.startsWith("data_");
}

function isMoneyScalarKey(key: PTituloDetailsScalarKey): boolean {
  return key.startsWith("valor_");
}

function getDefaultScalarValue(key: PTituloDetailsScalarKey, titulo: TituloListItem | null): string {
  const value = titulo?.[key as keyof TituloListItem];
  if (value === null || value === undefined) return "";
  if (isDateScalarKey(key)) return formatDateValue(value as Date | string | undefined);
  if (isMoneyScalarKey(key) && typeof value === "number") return formatMoneyValue(value);
  if (key === "tipo_aceite") return normalizePTituloTipoAceite(value);
  if (key === "tipo_endosso") return normalizePTituloTipoEndosso(value);
  return String(value);
}

export function getPTituloDetailsDefaultValues(titulo: TituloListItem | null): PTituloDetailsFormValues {
  const defaults = {} as Record<PTituloDetailsScalarKey, string | undefined>;

  for (const key of pTituloDetailsScalarKeys) {
    defaults[key] = getDefaultScalarValue(key, titulo);
  }

  return {
    ...defaults,
    partes: titulo?.vinculos_partes ?? [],
  } as PTituloDetailsFormValues;
}

export function formatPTituloFieldLabel(key: string): string {
  return key.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}
