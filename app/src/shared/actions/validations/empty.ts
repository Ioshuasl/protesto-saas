/**
 * Verifica se um valor é vazio, null ou undefined
 *
 * @param data - Qualquer valor
 * @returns true se estiver vazio, null ou undefined
 */
export default function empty(data: unknown): boolean {
  return data == null || data === '' || data === false;
}
