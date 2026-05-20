"use client";

import { z } from "zod";
import type { PTituloLiquidacaoFormInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloLiquidacaoFormInterface";
import { zPTituloWorkflowLocalIsoDate } from "@/packages/administrativo/schemas/PTitulo/PTituloWorkflowFormDateSchema";

type PTituloLiquidacaoFieldMap = Record<keyof PTituloLiquidacaoFormInterface, z.ZodTypeAny>;

const liquidacaoShape: PTituloLiquidacaoFieldMap = {
  ocorrencia_id: z.coerce.number().int().positive("Selecione a ocorrência"),
  motivo_cancelamento_id: z.coerce.number().int().positive("Selecione o motivo de cancelamento"),
  data_liquidacao: zPTituloWorkflowLocalIsoDate("Selecione a data de liquidação"),
  servico_gratuito: z.enum(["S", "N"]),
};

export const pTituloLiquidacaoFormSchema = z.object(liquidacaoShape);

export type PTituloLiquidacaoFormValues = z.infer<typeof pTituloLiquidacaoFormSchema>;
