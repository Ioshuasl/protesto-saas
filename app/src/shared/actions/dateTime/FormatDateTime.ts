/**
 * Formata uma data e hora brasileira (DD/MM/YYYY HH:mm)
 *
 * Suporta:
 * - Entrada como string, Date ou number (timestamp)
 * - Dados incompletos (apenas dia/mês, sem hora, etc.)
 * - Retorna "-" se vazio ou inválido
 *
 * @param value - Data ou hora em string, Date ou timestamp
 * @returns Data formatada no padrão DD/MM/YYYY HH:mm ou parcial
 */
export function FormatDateTime(value: string | Date | number | null | undefined): string {
  if (!value) return '-';

  let date: Date;

  // Converte entrada para Date
  if (value instanceof Date) {
    date = value;
  } else if (typeof value === 'number') {
    date = new Date(value);
  } else if (typeof value === 'string') {
    // Remove caracteres extras e tenta criar Date
    const cleanValue = value.trim().replace(/[^0-9]/g, '');

    if (cleanValue.length === 8) {
      // DDMMYYYY
      const day = parseInt(cleanValue.slice(0, 2), 10);
      const month = parseInt(cleanValue.slice(2, 4), 10) - 1;
      const year = parseInt(cleanValue.slice(4, 8), 10);
      date = new Date(year, month, day);
    } else {
      // Tenta parse padrão
      const parsed = new Date(value);
      if (isNaN(parsed.getTime())) return '-';
      date = parsed;
    }
  } else {
    return '-';
  }

  // Extrai partes da data
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');

  // Monta string parcialmente, dependendo da hora estar disponível
  const hasTime = !(hours === '00' && minutes === '00');

  return `${day}/${month}/${year}${hasTime ? ` ${hours}:${minutes}` : ''}`;
}
