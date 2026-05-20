"use client";

import { z } from "zod";
import type { PTituloVoltarApontamentoInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloVoltarApontamentoInterface";

type PTituloVoltarApontamentoFieldMap = Record<keyof PTituloVoltarApontamentoInterface, z.ZodTypeAny>;

const voltarApontamentoShape: PTituloVoltarApontamentoFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência"),
};

export const pTituloVoltarApontamentoSchema = z.object(voltarApontamentoShape);

export type PTituloVoltarApontamentoFormValues = z.infer<typeof pTituloVoltarApontamentoSchema>;

