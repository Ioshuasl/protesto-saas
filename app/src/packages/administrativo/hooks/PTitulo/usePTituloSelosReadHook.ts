import { useCallback, useState } from 'react';

import type { PTituloSeloVinculadoItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem';
import { PTituloSelosIndexService } from '@/packages/administrativo/services/PTitulo/PTituloSelosIndexService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTituloSelosReadHook = () => {
  const { setResponse } = useResponse();
  const [selos, setSelos] = useState<PTituloSeloVinculadoItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchSelos = useCallback(
    async (id: number) => {
      setIsLoading(true);
      try {
        const response = await PTituloSelosIndexService(id);
        if (Array.isArray(response)) {
          setSelos(response);
          setResponse({
            status: 200,
            message: 'Selos do título localizados com sucesso',
          });
        } else if (response && typeof response === 'object' && 'status' in response) {
          setSelos([]);
          setResponse({
            status: Number(response.status) || 600,
            message: String(response.message ?? 'Erro ao listar selos'),
            error: String(response.message ?? 'Erro ao listar selos'),
          });
        } else {
          setSelos([]);
        }
        return response;
      } finally {
        setIsLoading(false);
      }
    },
    [setResponse],
  );

  return { selos, setSelos, isLoading, fetchSelos };
};
