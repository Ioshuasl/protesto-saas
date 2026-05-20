"use client";

import { z } from "zod";
import type { PTituloProtestoInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloProtestoInterface";

type PTituloProtestoFieldMap = Record<keyof PTituloProtestoInterface, z.ZodTypeAny>;

const protestoShape: PTituloProtestoFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência de protesto"),
  data_protesto: z
    .string()
    .min(1, "Selecione a data de protesto")
    .refine((value) => /^\d{4}-\d{2}-\d{2}$/.test(value), "Data de protesto inválida")
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
    }, "Data de protesto inválida"),
};

export const pTituloProtestoSchema = z.object(protestoShape);

export type PTituloProtestoFormValues = z.infer<typeof pTituloProtestoSchema>;
