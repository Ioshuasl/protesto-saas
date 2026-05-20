/**
 * Converte o valor do input para número, enviando undefined se estiver vazio
 */
export function parseNumberInput(e: React.ChangeEvent<HTMLInputElement>): number | undefined {
  return e.target.value ? Number(e.target.value) : undefined;
}
