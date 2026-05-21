/** Extrai JWT de respostas de POST /administrativo/g_usuario/authenticate */
export function gUsuarioExtractAccessToken(
  response: Record<string, unknown>,
): string | undefined {
  const tokenKeys = ['token', 'access_token', 'accessToken'] as const;

  const pickFromObject = (record: Record<string, unknown>): string | undefined => {
    for (const key of tokenKeys) {
      const value = record[key];
      if (typeof value === 'string' && value.length > 0) {
        return value;
      }
    }
    return undefined;
  };

  const data = response.data;
  if (data && typeof data === 'object' && !Array.isArray(data)) {
    const record = data as Record<string, unknown>;
    const direct = pickFromObject(record);
    if (direct) {
      return direct;
    }
    const inner = record.data;
    if (inner && typeof inner === 'object' && !Array.isArray(inner)) {
      return pickFromObject(inner as Record<string, unknown>);
    }
  }

  const top = response.token;
  if (typeof top === 'string' && top.length > 0) {
    return top;
  }

  return undefined;
}

/** Login completo sem OTP (ex.: API_ENV=development com data.token) */
export function gUsuarioHasDirectAccessToken(response: Record<string, unknown>): boolean {
  return gUsuarioExtractAccessToken(response) !== undefined;
}

/** Só exibe GUsuarioAuth2FALoginForm quando a API pediu desafio OTP e não emitiu token */
export function gUsuarioRequiresTwoFactorStep(response: Record<string, unknown>): boolean {
  if (gUsuarioHasDirectAccessToken(response)) {
    return false;
  }

  const data = response.data;
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return false;
  }

  const record = data as Record<string, unknown>;
  return (
    record.two_factor_required === true && typeof record.usuario_id === 'number'
  );
}
