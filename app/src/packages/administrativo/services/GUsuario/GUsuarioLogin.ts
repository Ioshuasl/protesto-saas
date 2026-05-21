'use server';

import GUsuarioLoginData from '@/packages/administrativo/data/GUsuario/GUsuarioLoginData';
import type GUsuarioLoginChallengeInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioLoginChallengeInterface';
import { GUsuarioLoginFormValues } from '@/packages/administrativo/schemas/GUsuario/GUsuarioLoginSchema';
import { gUsuarioPersistAccessTokenAndRedirect } from '@/packages/administrativo/services/GUsuario/gUsuarioPersistAccessToken';
import {
  gUsuarioExtractAccessToken,
  gUsuarioRequiresTwoFactorStep,
} from '@/packages/administrativo/services/GUsuario/gUsuarioExtractAccessToken';

export type GUsuarioLoginFailure = { ok: false; message: string };

export type GUsuarioLoginRequiresTwoFactor = {
  ok: true;
  requiresTwoFactor: true;
  message: string;
  identificador: string;
  senha_api: string;
  data: Pick<
    GUsuarioLoginChallengeInterface,
    'usuario_id' | 'nome' | 'email' | 'challenge_expires_in'
  >;
};

export type GUsuarioLoginStepOneResult =
  | GUsuarioLoginFailure
  | GUsuarioLoginRequiresTwoFactor;

export default async function GUsuarioLoginService(
  form: GUsuarioLoginFormValues,
): Promise<GUsuarioLoginStepOneResult> {
  const response = (await GUsuarioLoginData(form)) as Record<string, unknown>;

  if (typeof response.status === 'number' && response.status >= 400) {
    return {
      ok: false,
      message:
        (typeof response.detail === 'string' ? response.detail : undefined) ??
        (typeof response.message === 'string' ? response.message : undefined) ??
        'Não foi possível autenticar',
    };
  }

  const token = gUsuarioExtractAccessToken(response);
  if (token) {
    await gUsuarioPersistAccessTokenAndRedirect(token);
  }

  if (gUsuarioRequiresTwoFactorStep(response)) {
    const data = response.data as Record<string, unknown>;

    return {
      ok: true,
      requiresTwoFactor: true,
      identificador: form.identificador.trim(),
      senha_api: form.senha_api,
      message:
        typeof response.message === 'string'
          ? response.message
          : 'Verificação em duas etapas necessária',
      data: {
        usuario_id: data.usuario_id as number,
        nome: (data.nome as string | null | undefined) ?? null,
        email: typeof data.email === 'string' ? data.email : '',
        challenge_expires_in:
          typeof data.challenge_expires_in === 'number'
            ? data.challenge_expires_in
            : 300,
      },
    };
  }

  return { ok: false, message: 'Resposta inesperada do servidor' };
}
