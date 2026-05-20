import * as z from "zod";

import { PBancoSimNao } from "@/packages/administrativo/interfaces/PBanco/PBancoInterface";

export const bancoFormSchema = z.object({
  codigo_banco: z.string().min(1, "Código do banco é obrigatório"),
  descricao: z.string().min(1, "Descrição é obrigatória"),
  layout_id: z.number().positive("Selecione um layout"),
  apontamento_pag_posterior: z.nativeEnum(PBancoSimNao),
  custas_na_confirmacao: z.nativeEnum(PBancoSimNao),
});

export type BancoFormValues = z.infer<typeof bancoFormSchema>;
