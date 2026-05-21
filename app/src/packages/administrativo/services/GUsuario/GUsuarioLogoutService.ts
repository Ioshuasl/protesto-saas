'use server';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export default async function GUsuarioLogoutService(token: string) {
  const cookieStore = await cookies();
  cookieStore.set(token, '', {
    expires: new Date(0),
    path: '/',
  });

  redirect('/login');
}
