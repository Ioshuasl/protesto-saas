'use server';

import { cookies } from 'next/headers';

/**
 * Função para obter tokens do lado servidorde acordo com o nome informado
 */
export default async function CookiesGet(token: string) {
  // Obtem a lista de Tokens
  const cookieStore = await cookies();

  // Obtem um token em especifico
  const data = cookieStore.get(token);

  // Retorna nulo ou o valor do token desejado
  return data?.value;
}
