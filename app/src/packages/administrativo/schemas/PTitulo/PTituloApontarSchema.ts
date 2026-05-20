"use client";

import { z } from "zod";
import type { PTituloApontarInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloApontarInterface";

type PTituloApontarFieldMap = Record<keyof PTituloApontarInterface, z.ZodTypeAny>;

const apontarShape: PTituloApontarFieldMap = {
  numero_apontamento: z.coerce.number().int().positive("Número de apontamento inválido").optional(),
  motivo_apontamento_id: z.coerce.number().int().positive("Selecione um motivo de apontamento"),
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência de intimado"),
  data_apontamento: z
    .string()
    .min(1, "Selecione a data de apontamento")
    .refine((value) => /^\d{4}-\d{2}-\d{2}$/.test(value), "Data de apontamento inválida")
    .refine((value) => {
      const [year, month, day] = value.split("-").map((part) => Number(part));
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
    }, "Data de apontamento inválida"),
};

export const pTituloApontarSchema = z.object(apontarShape);

export type PTituloApontarFormValues = z.infer<typeof pTituloApontarSchema>;

