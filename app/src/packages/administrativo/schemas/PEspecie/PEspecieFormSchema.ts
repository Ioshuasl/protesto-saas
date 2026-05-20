import * as z from "zod";

export const especieFormSchema = z.object({
  especie: z.string().min(1, "Sigla (espécie) é obrigatória"),
  descricao: z.string().min(1, "Descrição é obrigatória"),
});

export type EspecieFormValues = z.infer<typeof especieFormSchema>;
