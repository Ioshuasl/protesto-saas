"use client";

import { z } from "zod";
import type { PTituloIntimacaoInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloIntimacaoInterface";

type PTituloIntimacaoFieldMap = Record<keyof PTituloIntimacaoInterface, z.ZodTypeAny>;

const intimacaoShape: PTituloIntimacaoFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência de intimado"),
  data_intimacao: z
    .string()
    .min(1, "Selecione a data de intimação")
    .refine((value) => /^\d{4}-\d{2}-\d{2}$/.test(value), "Data de intimação inválida")
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
    }, "Data de intimação inválida"),
};

export const pTituloIntimacaoSchema = z.object(intimacaoShape);

export type PTituloIntimacaoFormValues = z.infer<typeof pTituloIntimacaoSchema>;

