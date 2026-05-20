"use client";

import { z } from "zod";
import type { PTituloTipoAceite } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";

export interface PTituloSelectOption<TValue extends string = string> {
  value: TValue;
  label: string;
}

/** Opções fixas de tipo de aceite (formulário de título). */
export const tituloTipoAceiteSelectOptions: PTituloSelectOption<PTituloTipoAceite>[] = [
  { value: "E", label: "Edital" },
  { value: "A", label: "Aceite" },
];

/** Opções Sim/Não usadas em campos string S/N do título. */
export const tituloBooleanSelectOptions: PTituloSelectOption[] = [
  { value: "S", label: "Sim" },
  { value: "N", label: "Não" },
];

/** Campos escalares do título persistidos como string no formulário (datas ISO yyyy-MM-dd, valores como texto, etc.). */
export const pTituloDetailsScalarKeys = [
  "titulo_id",
  "data_apontamento",
  "data_aceite",
  "valor_titulo",
  "data_protesto",
  "data_cancelamento",
  "especie_id",
  "ocorrencia_id",
  "numero_titulo",
  "data_vencimento_titulo",
  "data_emissao_titulo",
  "motivo_apontamento_id",
  "tabela_emolumento_id",
  "valor_emolumento",
  "valor_taxa_judiciaria",
  "valor_taxa_intimacao",
  "valor_desconto",
  "valor_taxa_edital",
  "valor_taxa_juros",
  "numero_apontamento",
  "data_cadastro",
  "motivo_cancelamento",
  "data_sustado",
  "folha_apontamento",
  "livro_id_apontamento",
  "user_assina_prot",
  "livro_id_protesto",
  "folha_protesto",
  "user_assina_apont",
  "data_pago",
  "valor_taxa_correios",
  "data_env_serasa",
  "data_ret_serasa",
  "valor_taxa_cancel",
  "valor_taxa_averb",
  "data_desistencia",
  "numero_cancelamento",
  "numero_protesto",
  "numero_ar",
  "taxa_correcao",
  "numero_titulo_banco",
  "data_mov_serasa",
  "nosso_numero",
  "valor_taxa_fundesp",
  "emolumento_item_id",
  "data_intimacao",
  "data_vencimento_boleto",
  "valor_total",
  "valor_iss",
  "nlote",
  "valor_total_custas",
  "banco_id",
  "agencia_centralizadora",
  "codigo_praca",
  "local_aceite",
  "observacoes",
  "situacao_aceite",
  "pessoa_aceitou",
  "agencia_correio",
  "praca_pagamento",
  "motivo_isencao",
  "prazo",
  "tipo_aceite",
  "numero_livro_apont",
  "tipo_endosso",
  "cobrar_juros",
  "letra_folha",
  "pagamento_posterior",
  "servico_gratuito",
  "pagamento_diferido",
  "titulo_antigo",
  "forma_pagamento",
  "agencia_codigo_cedente",
  "status_importacao",
  "protestado",
  "selecao_status",
  "importar",
  "nfse_id",
  "data_retorno_cda",
  "arquivo_titulo_id",
  "email",
  "data_anuencia",
  "origem_anuencia",
  "apresentante_permitido",
  "cedente_permitido",
  "credor_permitido",
  "anuencia",
  "situacao_cenprot",
  "custas_cancelamento_id",
  "livro_pagamento",
  "letra_livro_pagamento",
  "folha_livro_pagamento",
  "chave_unica_cenprot",
  "protesto_artigo_9",
  "chave_importacao",
  "impsituacao_titulo",
  "ocorrencia_andamento_id",
] as const;

export type PTituloDetailsScalarKey = (typeof pTituloDetailsScalarKeys)[number];

const tituloScalarShape = Object.fromEntries(
  pTituloDetailsScalarKeys.map((key) => [key, z.string().optional()]),
) as Record<PTituloDetailsScalarKey, z.ZodOptional<z.ZodString>>;

const pTituloParteItemSchema = z.object({
  pessoa_id: z.number().optional(),
  tipo: z.string(),
  descricao: z.string(),
  nome: z.string().optional(),
  cpfcnpj: z.string().optional(),
});

export const pTituloDetailsFormSchema = z.object({
  ...tituloScalarShape,
  partes: z.array(pTituloParteItemSchema),
});

export type PTituloDetailsFormValues = z.infer<typeof pTituloDetailsFormSchema>;

export type PTituloSelectOptionsByField = Partial<Record<PTituloDetailsScalarKey, PTituloSelectOption[]>>;
