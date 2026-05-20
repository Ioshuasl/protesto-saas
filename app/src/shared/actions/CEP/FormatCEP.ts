/**
 * Formata um número de CEP no padrão 99999-999
 *
 * @param value - CEP em string ou number
 * @returns CEP formatado ou string vazia se inválido
 */
export function FormatCEP(value: string | number): string {
  if (!value) return '';

  // Converte para string e remove tudo que não seja número
  const digits = String(value).replace(/\D/g, '');

  // Garante que tenha no máximo 8 dígitos
  const cleanValue = digits.slice(0, 8);

  // Retorna formatado ou valor limpo se não tiver tamanho suficiente
  if (cleanValue.length !== 8) return cleanValue;

  return cleanValue.replace(/(\d{5})(\d{3})/, '$1-$2');
}
