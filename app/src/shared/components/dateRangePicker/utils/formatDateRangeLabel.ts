export function formatDateRangeDay(date?: Date): string {
  if (!date) return "";
  return date.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}
