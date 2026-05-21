'use client';

import { useCallback, useState } from 'react';

import type GUsuarioMe from '@/packages/administrativo/interfaces/GUsuario/GUsuarioMeInterface';
import GUsuarioMeService from '@/packages/administrativo/services/GUsuario/GUsuarioMeService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGUsuarioMeHook = () => {
  const { setResponse } = useResponse();

  const [me, setMe] = useState<GUsuarioMe>();
  const [loading, setLoading] = useState(false);

  const fetchMe = useCallback(async () => {
    setLoading(true);
    try {
      const response = await GUsuarioMeService();
      if (typeof response.status === 'number' && response.status < 400 && response.data) {
        setMe(response.data as GUsuarioMe);
      } else {
        setMe(undefined);
      }
      setResponse(response);
    } finally {
      setLoading(false);
    }
  }, [setResponse]);

  return { me, loading, fetchMe };
};
