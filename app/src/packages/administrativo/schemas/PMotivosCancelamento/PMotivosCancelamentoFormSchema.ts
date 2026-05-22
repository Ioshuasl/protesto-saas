import * as z from "zod";

import { SituacoesEnum } from "@/shared/enums/SituacoesEnum";

const situacaoKeys = Object.keys(SituacoesEnum) as [keyof typeof SituacoesEnum, ...string[]];

export const motivoCancelamentoFormSchema = z.object({
  descricao: z.string().min(1, "Descrição é obrigatória"),
  situacao: z.enum(situacaoKeys, { message: "Situação é obrigatória" }),
});

export type MotivoCancelamentoFormValues = z.infer<typeof motivoCancelamentoFormSchema>;
