import * as z from "zod";

export const pessoaFormSchema = z
  .object({
    tipo_pessoa: z.enum(["F", "J"], { message: "Selecione o tipo de pessoa" }),
    cpfcnpj: z.string().min(14, "Documento inválido"),
    nome: z.string().min(1, "Nome/Razão Social é obrigatório"),
    rg: z.string().optional(),
    nacionalidade: z.string().optional(),
    estado_civil_id: z.number().optional(),
    data_nascimento: z.date().optional().nullable(),
    nome_fantasia: z.string().optional(),
    cod_cra: z.string().optional(),
    micro_empresa: z.string().optional(),
    cep: z.string().optional(),
    endereco: z.string().optional(),
    bairro: z.string().optional(),
    cidade: z.string().optional(),
    uf: z.string().optional(),
    telefone: z.string().optional(),
    email: z.string().email("E-mail inválido").optional().or(z.literal("")),
    banco: z.string().optional(),
    nome_banco: z.string().optional(),
    agencia: z.string().optional(),
    conta: z.string().optional(),
    cidade_agencia: z.string().optional(),
    observacoes: z.string().optional(),
  })
  .superRefine((data, ctx) => {
    const docLength = data.cpfcnpj.replace(/\D/g, "").length;
    const isPessoaFisica = data.tipo_pessoa === "F";
    const isPessoaJuridica = data.tipo_pessoa === "J";

    if (isPessoaFisica) {
      if (docLength !== 11) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "CPF deve conter 11 dígitos", path: ["cpfcnpj"] });
      }
      if (!data.rg) ctx.addIssue({ code: z.ZodIssueCode.custom, message: "RG é obrigatório para CPF", path: ["rg"] });
      if (!data.nacionalidade)
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Nacionalidade é obrigatória para CPF", path: ["nacionalidade"] });
      if (!data.estado_civil_id)
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Estado Civil é obrigatório para CPF", path: ["estado_civil_id"] });
      if (!data.data_nascimento)
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Data de Nascimento é obrigatória para CPF", path: ["data_nascimento"] });
    } else if (isPessoaJuridica) {
      if (docLength !== 14) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "CNPJ deve conter 14 dígitos", path: ["cpfcnpj"] });
      }
      if (!data.nome_fantasia)
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Nome Fantasia é obrigatório para CNPJ", path: ["nome_fantasia"] });
      if (!data.cod_cra) ctx.addIssue({ code: z.ZodIssueCode.custom, message: "CRA é obrigatório para CNPJ", path: ["cod_cra"] });
    }
  });

export type PessoaFormSchemaValues = z.infer<typeof pessoaFormSchema>;
export type PessoaFormValues = Omit<PessoaFormSchemaValues, "tipo_pessoa">;
