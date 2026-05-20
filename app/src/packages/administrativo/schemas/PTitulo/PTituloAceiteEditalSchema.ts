"use client";

import { z } from "zod";
import type { PTituloAceiteEditalInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloAceiteEditalInterface";

type PTituloAceiteEditalFieldMap = Record<keyof PTituloAceiteEditalInterface, z.ZodTypeAny>;

const aceiteEditalShape: PTituloAceiteEditalFieldMap = {
  devedores: z
    .array(
      z.object({
        pessoa_vinculo_id: z.coerce.number().int().positive("Vínculo do devedor inválido"),
        devedor_tipo_aceite: z.enum(["A", "E"], "Selecione Aceite ou Edital"),
        devedor_data_aceite: z
          .string()
          .min(1, "Selecione a data de aceite/edital")
          .refine((value) => /^\d{4}-\d{2}-\d{2}$/.test(value), "Data de aceite/edital inválida")
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
          }, "Data de aceite/edital inválida"),
      }),
    )
    .min(1, "É necessário selecionar ao menos um devedor"),
};

export const pTituloAceiteEditalSchema = z.object(aceiteEditalShape);

export type PTituloAceiteEditalFormValues = z.infer<typeof pTituloAceiteEditalSchema>;

