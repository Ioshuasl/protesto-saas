/**
 * Remove caracteres não numéricos (Auxiliar)
 * Se você já tiver essa função exportada em outro lugar, pode importar.
 */
function unmask(value: string): string {
  return value.replace(/\D/g, '');
}

export function FormatDateForm(value: string = ''): string {
  const digits = unmask(value);

  return digits
    .slice(0, 8) // Limita a 8 dígitos (ddmmyyyy)
    .replace(/^(\d{2})(\d)/, '$1/$2') // Coloca a primeira barra após o dia
    .replace(/^(\d{2})\/(\d{2})(\d)/, '$1/$2/$3'); // Coloca a segunda barra após o mês
}
