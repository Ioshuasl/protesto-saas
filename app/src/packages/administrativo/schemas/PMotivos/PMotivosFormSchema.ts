import * as z from "zod";

import { SituacoesEnum } from "@/shared/enums/SituacoesEnum";

const situacaoKeys = Object.keys(SituacoesEnum) as [keyof typeof SituacoesEnum, ...string[]];

export const motivoFormSchema = z.object({
  codigo: z.string().min(1, "Código é obrigatório").max(3, "Código deve ter no máximo 3 caracteres"),
  descricao: z.string().min(1, "Descrição é obrigatória"),
  situacao: z.enum(situacaoKeys, { message: "Situação é obrigatória" }),
});

export type MotivoFormValues = z.infer<typeof motivoFormSchema>;
