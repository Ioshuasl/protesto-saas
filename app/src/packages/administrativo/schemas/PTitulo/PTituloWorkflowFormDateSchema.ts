"use client";

import { z } from "zod";

function isValidCalendarLocalParts(year: number, month: number, day: number): boolean {
  if (
    Number.isNaN(year) ||
    Number.isNaN(month) ||
    Number.isNaN(day) ||
    year <= 0 ||
    month <= 0 ||
    day <= 0
  ) {
    return false;
  }
  const localDate = new Date(year, month - 1, day);
  return (
    localDate.getFullYear() === year &&
    localDate.getMonth() === month - 1 &&
    localDate.getDate() === day
  );
}

/** Campo de data no formato `yyyy-MM-dd` (mesmo padrão de PTituloApontarSchema). */
export function zPTituloWorkflowLocalIsoDate(emptyMessage: string, invalidMessage = "Data inválida") {
  return z
    .string()
    .min(1, emptyMessage)
    .refine((value) => /^\d{4}-\d{2}-\d{2}$/.test(value), invalidMessage)
    .refine((value) => {
      const [year, month, day] = value.split("-").map((part) => Number(part));
      return isValidCalendarLocalParts(year, month, day);
    }, invalidMessage);
}
