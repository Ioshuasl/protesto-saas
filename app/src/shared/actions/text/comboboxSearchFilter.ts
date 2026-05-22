/**
 * Normaliza texto para busca: remove acentos, padroniza caixa e espaços.
 */
export function normalizeSearchText(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim()
    .replace(/\s+/g, " ");
}

/**
 * Verifica se `haystack` contém todos os termos de `needle`
 * (busca abrangente: acentos, maiúsculas/minúsculas, múltiplas palavras).
 */
export function matchesSearchText(haystack: string, needle: string): boolean {
  const normalizedHaystack = normalizeSearchText(haystack);
  const normalizedNeedle = normalizeSearchText(needle);

  if (!normalizedNeedle) return true;

  const terms = normalizedNeedle.split(" ").filter(Boolean);
  return terms.every((term) => normalizedHaystack.includes(term));
}

/**
 * Filtro do cmdk (`Command`): retorna 1 quando há correspondência, 0 caso contrário.
 */
export function comboboxSearchFilter(value: string, search: string): number {
  return matchesSearchText(value, search) ? 1 : 0;
}
