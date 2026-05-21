'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export async function gUsuarioPersistAccessTokenAndRedirect(token: string): Promise<never> {
  const cookieStore = await cookies();

  cookieStore.set('access_token', token, {
    httpOnly: true,
    secure: false,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60 * 24,
  });

  redirect('/');
}
