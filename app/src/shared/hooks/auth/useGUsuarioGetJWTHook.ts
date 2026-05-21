'use client';

import { jwtDecode } from 'jwt-decode';
import { useCallback, useState } from 'react';

import GetSigla from '@/shared/actions/text/GetSigla';
import GUsuarioAuthenticatedInterface from '@/shared/interfaces/GUsuarioAuthenticatedInterface';

import CookiesGet from '../../actions/cookies/CookiesGet';

interface JwtPayload {
  id: string;
  iat: number;
  exp: number;
  data?: GUsuarioAuthenticatedInterface;
}

export default function useGUsuarioGetJWTHook() {
  const [userAuthenticated, setUserAuthenticated] = useState<JwtPayload | null>(null);

  const fetchToken = useCallback(async () => {
    const token = await CookiesGet('access_token');

    if (!token) {
      console.error('Não foi localizado dados dentro do token');
      return null;
    }

    const decoded = jwtDecode<JwtPayload>(token);

    if (decoded.data && typeof decoded.data === 'string') {
      decoded.data = JSON.parse(decoded.data);

      if (decoded.data) {
        decoded.data.sigla = GetSigla(decoded.data.nome || '');
      }
    }

    setUserAuthenticated(decoded);

    return decoded;
  }, []);

  return { userAuthenticated, fetchToken };
}
