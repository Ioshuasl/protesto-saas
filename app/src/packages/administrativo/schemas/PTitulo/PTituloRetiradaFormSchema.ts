"use client";

import { z } from "zod";
import type { PTituloRetiradaFormInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloRetiradaFormInterface";
import { zPTituloWorkflowLocalIsoDate } from "@/packages/administrativo/schemas/PTitulo/PTituloWorkflowFormDateSchema";

type PTituloRetiradaFieldMap = Record<keyof PTituloRetiradaFormInterface, z.ZodTypeAny>;

const retiradaShape: PTituloRetiradaFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência"),
  motivo_cancelamento_id: z.coerce.number().int().positive("Selecione o motivo de cancelamento"),
  data_retirada: zPTituloWorkflowLocalIsoDate("Selecione a data de retirada"),
  servico_gratuito: z.enum(["S", "N"]),
};

export const pTituloRetiradaFormSchema = z.object(retiradaShape);

export type PTituloRetiradaFormValues = z.infer<typeof pTituloRetiradaFormSchema>;
