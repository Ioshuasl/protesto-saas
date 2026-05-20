/**
 * Formata um número de telefone brasileiro.
 *
 * Suporta:
 * - Com ou sem DDD
 * - Números incompletos
 * - Telefones com 8 ou 9 dígitos
 *
 * @param value - Número de telefone em string ou number
 * @returns Telefone formatado ou "-" se vazio
 */
export function FormatPhone(value: string | number): string {
  if (!value) return '-';

  // Converte para string e remove tudo que não for número
  const digits = String(value).replace(/\D/g, '');

  // Se não tiver nada após limpar, retorna "-"
  if (digits.length === 0) return '-';

  // Garante no máximo 11 dígitos
  const cleanValue = digits.slice(0, 11);

  // -------------------------------
  // SEM DDD
  // -------------------------------
  if (cleanValue.length <= 8) {
    // Até 8 dígitos → formato parcial
    return cleanValue.replace(/(\d{4})(\d{0,4})/, '$1-$2').replace(/-$/, '');
  }

  // -------------------------------
  // COM DDD
  // -------------------------------
  if (cleanValue.length === 9 || cleanValue.length === 10) {
    // DDD + telefone de 8 dígitos
    return cleanValue.replace(/^(\d{2})(\d{4})(\d{0,4})$/, '($1) $2-$3').replace(/-$/, '');
  }

  if (cleanValue.length === 11) {
    // DDD + telefone de 9 dígitos
    return cleanValue.replace(/^(\d{2})(\d{5})(\d{0,4})$/, '($1) $2-$3').replace(/-$/, '');
  }

  // Caso genérico, se não cair em nenhuma regra
  return cleanValue;
}
