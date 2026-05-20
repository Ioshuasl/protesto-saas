/**
 * Capitaliza a primeira letra de uma string.
 *
 * @param text - Texto que será capitalizado
 * @returns String com a primeira letra em maiúscula
 */
export default function GetCapitalize(text?: string): string {
  if (!text) return '';

  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}
