"use client";

import { z } from "zod";
import type { PTituloDesistenciaFormInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloDesistenciaFormInterface";
import { zPTituloWorkflowLocalIsoDate } from "@/packages/administrativo/schemas/PTitulo/PTituloWorkflowFormDateSchema";

type PTituloDesistenciaFieldMap = Record<keyof PTituloDesistenciaFormInterface, z.ZodTypeAny>;

const desistenciaShape: PTituloDesistenciaFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência"),
  motivo_cancelamento_id: z.coerce.number().int().positive("Selecione o motivo de cancelamento"),
  data_desistencia: zPTituloWorkflowLocalIsoDate("Selecione a data de desistência"),
  servico_gratuito: z.enum(["S", "N"]),
};

export const pTituloDesistenciaFormSchema = z.object(desistenciaShape);

export type PTituloDesistenciaFormValues = z.infer<typeof pTituloDesistenciaFormSchema>;
