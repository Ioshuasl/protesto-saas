"use client";

import { z } from "zod";
import type { PTituloCancelamentoFormInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloCancelamentoFormInterface";
import { zPTituloWorkflowLocalIsoDate } from "@/packages/administrativo/schemas/PTitulo/PTituloWorkflowFormDateSchema";

type PTituloCancelamentoFieldMap = Record<keyof PTituloCancelamentoFormInterface, z.ZodTypeAny>;

const cancelamentoShape: PTituloCancelamentoFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência"),
  motivo_cancelamento_id: z.coerce.number().int().positive("Selecione o motivo de cancelamento"),
  data_cancelamento: zPTituloWorkflowLocalIsoDate("Selecione a data de cancelamento"),
  servico_gratuito: z.enum(["S", "N"]),
};

export const pTituloCancelamentoFormSchema = z.object(cancelamentoShape);

export type PTituloCancelamentoFormValues = z.infer<typeof pTituloCancelamentoFormSchema>;
