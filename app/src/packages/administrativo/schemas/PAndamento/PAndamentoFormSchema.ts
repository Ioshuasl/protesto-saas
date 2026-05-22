import * as z from 'zod';

import {
  ARQUIVO_GERADO_AGUARDANDO,
  ARQUIVO_GERADO_EXPORTADO,
} from '@/packages/administrativo/schemas/PAndamento/pAndamentoArquivoGeradoConstants';

const arquivoGeradoEnum = z.enum([ARQUIVO_GERADO_AGUARDANDO, ARQUIVO_GERADO_EXPORTADO], {
  message: 'Use D (aguardando) ou E (exportado)',
});

export const pAndamentoFormSchema = z.object({
  ocorrencia_andamento_id: z.number().min(1, 'Ocorrência de andamento é obrigatória'),
  titulo_id: z.number().min(1, 'Título é obrigatório'),
  usuario_id: z.number().min(1, 'Usuário é obrigatório'),
  data_ocorrencia: z.date({
    message: 'Data de ocorrência é obrigatória',
  }),
  arquivo_gerado: arquivoGeradoEnum.default(ARQUIVO_GERADO_AGUARDANDO),
  data_geracao: z.date().optional().nullable(),
});

export type PAndamentoFormValues = z.infer<typeof pAndamentoFormSchema>;
