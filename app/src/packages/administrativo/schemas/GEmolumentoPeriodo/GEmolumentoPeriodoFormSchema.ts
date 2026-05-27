import * as z from "zod";

export const gEmolumentoPeriodoFormSchema = z.object({
  descricao: z.string().min(1, "Descricao e obrigatoria"),
  situacao: z.enum(["A", "I"], {
    message: "Situacao e obrigatoria",
  }),
  data_inicial: z.date({
    message: "Data inicial e obrigatoria",
  }),
});

export type GEmolumentoPeriodoFormValues = z.infer<typeof gEmolumentoPeriodoFormSchema>;
