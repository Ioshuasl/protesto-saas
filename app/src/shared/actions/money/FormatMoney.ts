export default function FormatMoney(data?: number | string | null): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(Number(data || 0));
}
