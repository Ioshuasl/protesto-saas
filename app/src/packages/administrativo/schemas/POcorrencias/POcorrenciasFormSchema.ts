import * as z from "zod";

export const ocorrenciaFormSchema = z.object({
  codigo: z.string().min(1, "Código é obrigatório"),
  tipo: z.string().min(1, "Tipo é obrigatório"),
  descricao: z.string().min(1, "Descrição é obrigatória"),
});

export type OcorrenciaFormValues = z.infer<typeof ocorrenciaFormSchema>;
