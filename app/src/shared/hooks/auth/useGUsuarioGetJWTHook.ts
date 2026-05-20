'use client';

import { jwtDecode } from 'jwt-decode';
import { useState } from 'react';

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

  async function fetchToken() {
    // Executa a serve action para obtem o token, salvo em cookies
    const token = await CookiesGet('access_token');

    // Verifica se o token esta preenchido
    if (!token) {
      console.error('Não foi localizado dados dentro do token');

      // Encerra a aplicação
      return;
    }

    // Decodifica os dados do JWT
    const decoded = jwtDecode<JwtPayload>(token);

    // Se existir campo data e for string, corrige aspas simples
    if (decoded.data && typeof decoded.data === 'string') {
      // Decodifica os dados enviado via json
      decoded.data = JSON.parse(decoded.data);

      if (decoded.data) {
        // Gera Sigla para o nome
        decoded.data.sigla = GetSigla(decoded.data.nome || '');
      }
    }

    // Armazena os dados decodificados
    setUserAuthenticated(decoded);

    return decoded;
  }

  return { userAuthenticated, fetchToken };
}
