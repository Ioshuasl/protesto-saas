'use server';

import GUsuarioAuth2FAData from '@/packages/administrativo/data/GUsuario/GUsuarioAuth2FAData';
import type { GUsuarioAuth2FARequestPayload } from '@/packages/administrativo/data/GUsuario/GUsuarioAuth2FAData';
import { gUsuarioPersistAccessTokenAndRedirect } from '@/packages/administrativo/services/GUsuario/gUsuarioPersistAccessToken';
import {
  gUsuarioExtractAccessToken,
  gUsuarioRequiresTwoFactorStep,
} from '@/packages/administrativo/services/GUsuario/gUsuarioExtractAccessToken';

export type GUsuarioAuth2FAServiceDebug = {
  httpStatus: number;
  responseKeys: string[];
  dataTipo: string;
  dataKeys: string[] | null;
  apiMessage?: string;
  detail?: unknown;
  repeatChallengePayload?: boolean;
};

export type GUsuarioAuth2FAServiceError = {
  ok: false;
  message: string;
  debug?: GUsuarioAuth2FAServiceDebug;
};

function dataLooksLikeFirstStepChallenge(response: Record<string, unknown>): boolean {
  return gUsuarioRequiresTwoFactorStep(response);
}

function snapshotResponse(response: Record<string, unknown>): GUsuarioAuth2FAServiceDebug {
  const data = response.data;
  let dataTipo = data === null ? 'null' : Array.isArray(data) ? 'array' : typeof data;
  let dataKeys: string[] | null = null;
  if (data !== undefined && data !== null && typeof data === 'object' && !Array.isArray(data)) {
    dataKeys = Object.keys(data as object);
  }

  return {
    httpStatus: typeof response.status === 'number' ? response.status : -1,
    responseKeys: Object.keys(response),
    dataTipo,
    dataKeys,
    apiMessage: typeof response.message === 'string' ? response.message : undefined,
    detail: response.detail,
  };
}

export default async function GUsuarioAuth2FAService(
  payload: GUsuarioAuth2FARequestPayload,
): Promise<GUsuarioAuth2FAServiceError | undefined> {
  const response = (await GUsuarioAuth2FAData(payload)) as Record<string, unknown>;
  const debug = snapshotResponse(response);

  if (typeof response.status === 'number' && response.status >= 400) {
    console.warn('[GUsuarioAuth2FA Service] HTTP de erro', debug);
    return {
      ok: false,
      message:
        (typeof response.detail === 'string' ? response.detail : undefined) ??
        (typeof response.message === 'string' ? response.message : undefined) ??
        'Falha na verificação em duas etapas',
      debug,
    };
  }

  const token = gUsuarioExtractAccessToken(response);
  if (!token) {
    const repeatChallenge = dataLooksLikeFirstStepChallenge(response);
    console.warn('[GUsuarioAuth2FA Service] token não encontrado na resposta', {
      ...debug,
      repeatChallengePayload: repeatChallenge,
    });

    return {
      ok: false,
      message: repeatChallenge
        ? 'O servidor devolveu o mesmo desafio 2FA (sem token). Verifique o código ou tente login novamente.'
        : 'Token não recebido. Verifique o código ou o formato da resposta da API.',
      debug: { ...debug, repeatChallengePayload: repeatChallenge },
    };
  }

  await gUsuarioPersistAccessTokenAndRedirect(token);
}
