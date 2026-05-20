import * as z from "zod";

export const motivoCancelamentoFormSchema = z.object({
  descricao: z.string().min(1, "Descrição é obrigatória"),
  situacao: z.string().min(1, "Situação é obrigatória"),
  ord_jud_ou_rem_ind: z.enum(["Ordem Judicial", "Remessa Indireta", "Outros"], {
    message: "Tipo é obrigatório",
  }),
});

export type MotivoCancelamentoFormValues = z.infer<typeof motivoCancelamentoFormSchema>;
