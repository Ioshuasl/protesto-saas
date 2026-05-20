/**
 * Formata um número de CPF no padrão 999.999.999-99
 *
 * @param value - CPF em string ou number
 * @returns CPF formatado ou string vazia se inválido
 */
export function FormatCPF(value?: string | number): string {
  if (!value) return '';

  // Converte para string e remove tudo que não seja número
  const digits = String(value).replace(/\D/g, '');

  // Garante que tenha no máximo 11 dígitos
  const cleanValue = digits.slice(0, 11);

  // Retorna formatado ou vazio se não tiver tamanho suficiente
  if (cleanValue.length !== 11) return cleanValue;

  return cleanValue.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}
