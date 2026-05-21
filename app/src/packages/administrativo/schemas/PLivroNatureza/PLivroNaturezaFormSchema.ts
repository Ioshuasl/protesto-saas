import * as z from "zod";

import { SituacoesEnum } from "@/shared/enums/SituacoesEnum";

const situacaoKeys = Object.keys(SituacoesEnum) as [keyof typeof SituacoesEnum, ...string[]];

export const livroNaturezaFormSchema = z.object({
  sigla: z.string().min(1, "Sigla é obrigatória").max(3, "Sigla deve ter no máximo 3 caracteres"),
  descricao: z.string().min(1, "Descrição é obrigatória"),
  situacao: z.enum(situacaoKeys, { message: "Situação é obrigatória" }),
});

export type LivroNaturezaFormValues = z.infer<typeof livroNaturezaFormSchema>;
