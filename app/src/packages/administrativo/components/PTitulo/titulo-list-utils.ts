"use client";

import { addBusinessDays, differenceInBusinessDays } from "date-fns";
import { TituloListItem } from "@/packages/administrativo/services/PTitulo/PTituloService";

export const moneyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

export function formatDateBr(value: Date | string | undefined): string {
  if (!value) return "-";
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return "-";
  return date.toLocaleDateString("pt-BR");
}

export function toInputDate(value: Date | string | undefined): string {
  if (!value) return "";
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

/** Valor inicial `S`/`N` para Serviço gratuito (mesma convenção de `PTituloFeesSection`). */
export function tituloServicoGratuitoSn(titulo?: { servico_gratuito?: string | null }): "S" | "N" {
  const v = titulo?.servico_gratuito;
  if (v === "S" || v === "true" || v === "1") return "S";
  return "N";
}

export function getTriduoMessage(titulo: TituloListItem): string | null {
  if (!titulo.data_intimacao) return null;
  const status = (titulo.status_descricao ?? titulo.situacao_aceite ?? "").toLowerCase();
  const isOpen =
    !status.includes("protest") &&
    !status.includes("pag") &&
    !status.includes("liquid") &&
    !status.includes("cancel");
  if (!isOpen) return null;

  const intimacaoDate = new Date(titulo.data_intimacao as unknown as string);
  if (Number.isNaN(intimacaoDate.getTime())) return null;

  const deadline = addBusinessDays(intimacaoDate, 3);
  const remaining = differenceInBusinessDays(deadline, new Date());

  if (remaining < 0) return "Prazo do tríduo vencido";
  if (remaining === 0) return "Último dia do tríduo";
  return `Faltam ${remaining} dia(s)`;
}
