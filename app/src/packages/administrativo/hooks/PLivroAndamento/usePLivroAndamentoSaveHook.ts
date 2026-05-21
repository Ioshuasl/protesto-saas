import { useState } from 'react';

import { formatDateTimeForApi } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoApiUtils';
import { invalidateProximoNumeroCache } from '@/packages/administrativo/hooks/PLivroAndamento/useProximoNumeroPorNatureza';
import type { PLivroAndamentoSavePayload } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoSaveData';
import { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { LivroAndamentoFormValues } from '@/packages/administrativo/schemas/PLivroAndamento/PLivroAndamentoFormSchema';
import { PLivroAndamentoSaveCreateService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoSaveCreateService';
import { PLivroAndamentoSaveUpdateService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

function buildSavePayload(data: LivroAndamentoFormValues): PLivroAndamentoSavePayload {
  return {
    livro_natureza_id: data.livro_natureza_id,
    folha_atual: data.folha_atual,
    numero_livro: data.numero_livro,
    numero_folhas: data.numero_folhas,
    data_abertura: formatDateTimeForApi(data.data_abertura),
    data_fechamento:
      data.data_fechamento != null ? formatDateTimeForApi(data.data_fechamento) : null,
    sigla: data.sigla?.trim() || undefined,
    usuario_id: data.usuario_id ?? null,
  };
}

export const usePLivroAndamentoSaveHook = () => {
  const { setResponse } = useResponse();
  const [pLivroAndamento, setPLivroAndamento] = useState<PLivroAndamentoInterface | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const saveLivroAndamento = async (
    data: LivroAndamentoFormValues,
    selected: PLivroAndamentoInterface | null,
  ) => {
    const payload = buildSavePayload(data);

    const response = selected
      ? await PLivroAndamentoSaveUpdateService(selected.livro_andamento_id, payload)
      : await PLivroAndamentoSaveCreateService(payload);

    if (response && typeof response === 'object' && 'livro_andamento_id' in response) {
      setPLivroAndamento(response as PLivroAndamentoInterface);
      invalidateProximoNumeroCache(payload.livro_natureza_id);
    }

    setResponse(
      response && typeof response === 'object' && 'livro_andamento_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected
              ? 'Livro em andamento atualizado com sucesso'
              : 'Livro em andamento criado com sucesso',
          }
        : {
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          },
    );

    setIsOpen(false);

    return response;
  };

  return { pLivroAndamento, saveLivroAndamento, isOpen, setIsOpen };
};
