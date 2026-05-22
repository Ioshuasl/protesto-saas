import * as z from 'zod';

import {
  POCORRENCIAS_TIPO_OPCOES,
  type POcorrenciasTipoOpcao,
} from '@/packages/administrativo/schemas/POcorrencias/pocorrenciasTipoConstants';

const tipoOpcoesSet = new Set<string>(POCORRENCIAS_TIPO_OPCOES);

export const ocorrenciaFormSchema = z.object({
  codigo: z.string().min(1, 'Código é obrigatório'),
  descricao: z.string().min(1, 'Descrição é obrigatória'),
  tipo: z
    .string()
    .optional()
    .refine(
      (value) => !value || value.trim() === '' || tipoOpcoesSet.has(value),
      'Selecione um tipo válido ou deixe em branco',
    ),
});

export type OcorrenciaFormValues = z.infer<typeof ocorrenciaFormSchema>;

export function formValuesToApiPayload(data: OcorrenciaFormValues): {
  codigo: string;
  descricao: string;
  tipo?: POcorrenciasTipoOpcao;
} {
  const tipo = data.tipo?.trim();
  return {
    codigo: data.codigo.trim(),
    descricao: data.descricao.trim(),
    ...(tipo ? { tipo: tipo as POcorrenciasTipoOpcao } : {}),
  };
}
