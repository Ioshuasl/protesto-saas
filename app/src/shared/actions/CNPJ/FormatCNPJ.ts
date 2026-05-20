/**
 * Formata um número de CNPJ no padrão 99.999.999/9999-99
 *
 * @param value - CNPJ em string ou number
 * @returns CNPJ formatado ou string parcial se incompleto
 */
export function FormatCNPJ(value: string | number): string {
  if (!value) return '';

  // Converte para string e remove tudo que não seja número
  const digits = String(value).replace(/\D/g, '');

  // Garante que tenha no máximo 14 dígitos
  const cleanValue = digits.slice(0, 14);

  // Retorna parcialmente formatado se ainda não tiver 14 dígitos
  if (cleanValue.length < 14) return cleanValue;

  return cleanValue.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
}
