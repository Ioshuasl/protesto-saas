"use client";

import { z } from "zod";
import type { PTituloVoltarIntimacaoInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloVoltarIntimacaoInterface";

type PTituloVoltarIntimacaoFieldMap = Record<keyof PTituloVoltarIntimacaoInterface, z.ZodTypeAny>;

const voltarIntimacaoShape: PTituloVoltarIntimacaoFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência"),
};

export const pTituloVoltarIntimacaoSchema = z.object(voltarIntimacaoShape);

export type PTituloVoltarIntimacaoFormValues = z.infer<typeof pTituloVoltarIntimacaoSchema>;

