'use client';

import { useCallback, useState } from 'react';

import type { GUsuarioAuth2FARequestPayload } from '@/packages/administrativo/data/GUsuario/GUsuarioAuth2FAData';
import GUsuarioAuth2FAService, {
  type GUsuarioAuth2FAServiceError,
} from '@/packages/administrativo/services/GUsuario/GUsuarioAuth2FAService';

export function useGUsuarioAuth2FAHook() {
  const [loading, setLoading] = useState(false);

  const verifyAuth2FA = useCallback(async (payload: GUsuarioAuth2FARequestPayload) => {
    setLoading(true);

    try {
      const result = await GUsuarioAuth2FAService(payload);

      if (result?.ok === false) {
        console.groupCollapsed('[GUsuario Auth2FA] erro retornado pelo servidor');
        console.log('message', result.message);
        if (result.debug) {
          console.log('debug (shape da resposta da API)', result.debug);
        } else {
          console.log('debug não disponível');
        }
        console.groupEnd();
      } else if (result === undefined) {
        // Sucesso: redirect do server action costuma interromper antes do cliente receber valor
        console.info('[GUsuario Auth2FA] fluxo concluído (redirect em curso ou sessão atualizada)');
      }

      return result as GUsuarioAuth2FAServiceError | undefined;
    } catch (error) {
      console.groupCollapsed('[GUsuario Auth2FA] exceção ao chamar o server action');
      console.error(error);
      console.groupEnd();
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return { verifyAuth2FA, loading };
}
