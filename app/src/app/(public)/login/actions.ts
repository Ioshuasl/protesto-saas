'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

/** JWT mínimo (3 segmentos) só para o middleware ler `exp` — não é autenticação real. */
function buildDevAccessToken(expSeconds: number): string {
  const header = Buffer.from(JSON.stringify({ alg: 'none', typ: 'JWT' })).toString('base64url');
  const payload = Buffer.from(JSON.stringify({ exp: expSeconds, sub: 'dev-local' })).toString('base64url');
  return `${header}.${payload}.dev`;
}

/** Define sessão fictícia e envia para o app protegido. */
export async function signInAsDev() {
  const maxAgeSeconds = 60 * 60 * 24 * 365;
  const exp = Math.floor(Date.now() / 1000) + maxAgeSeconds;
  const token = buildDevAccessToken(exp);

  const cookieStore = await cookies();
  cookieStore.set('access_token', token, {
    path: '/',
    maxAge: maxAgeSeconds,
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
  });

  redirect('/');
}
