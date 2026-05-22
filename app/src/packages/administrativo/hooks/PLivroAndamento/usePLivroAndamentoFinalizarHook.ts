import { useState } from 'react';

import { formatDateTimeForApi } from '@/packages/administrativo/data/PLivroAndamento/plivroAndamentoApiUtils';
import type { PLivroAndamentoFinalizarPayload } from '@/packages/administrativo/data/PLivroAndamento/PLivroAndamentoFinalizarData';
import { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import { PLivroAndamentoFinalizarService } from '@/packages/administrativo/services/PLivroAndamento/PLivroAndamentoFinalizarService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export type PLivroAndamentoFinalizarInput = {
  data_fechamento: Date;
  folha_atual?: number;
  usuario_id?: number | null;
};

function buildFinalizarPayload(data: PLivroAndamentoFinalizarInput): PLivroAndamentoFinalizarPayload {
  return {
    data_fechamento: formatDateTimeForApi(data.data_fechamento),
    ...(data.folha_atual !== undefined ? { folha_atual: data.folha_atual } : {}),
    ...(data.usuario_id !== undefined ? { usuario_id: data.usuario_id } : {}),
  };
}

export const usePLivroAndamentoFinalizarHook = () => {
  const { setResponse } = useResponse();
  const [pLivroAndamento, setPLivroAndamento] = useState<PLivroAndamentoInterface | null>(null);

  const finalizarLivroAndamento = async (
    id: number,
    data: PLivroAndamentoFinalizarInput,
  ) => {
    const payload = buildFinalizarPayload(data);
    const response = await PLivroAndamentoFinalizarService(id, payload);

    if (response && typeof response === 'object' && 'livro_andamento_id' in response) {
      setPLivroAndamento(response as PLivroAndamentoInterface);
      setResponse({
        status: 200,
        message: 'Livro em andamento finalizado com sucesso',
      });
    } else {
      setResponse({
        status: (response as { status?: number }).status,
        message: (response as { message?: string }).message,
        error: (response as { message?: string }).message,
      });
    }

    return response;
  };

  return { pLivroAndamento, finalizarLivroAndamento };
};
