import * as z from "zod";

export const livroAndamentoFormSchema = z.object({
  numero_livro: z.number().min(1, "Número do livro é obrigatório"),
  livro_natureza_id: z.number().min(1, "Natureza do livro é obrigatória"),
  folha_atual: z.number().min(0, "Folha atual é obrigatória"),
  numero_folhas: z.number().min(1, "Número de folhas é obrigatório"),
  data_abertura: z.date({
    message: "Data de abertura é obrigatória",
  }),
  data_fechamento: z.date().optional().nullable(),
  sigla: z.string().min(1, "Sigla é obrigatória"),
  usuario_id: z.number().optional().nullable(),
});

export type LivroAndamentoFormValues = z.infer<typeof livroAndamentoFormSchema>;
