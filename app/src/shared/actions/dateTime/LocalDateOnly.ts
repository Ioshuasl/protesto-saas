import { FormatDateForm } from '@/shared/actions/dateTime/FormatDateForm';

function isValidLocalDateParts(year: number, month: number, day: number): boolean {
  if (
    Number.isNaN(year) ||
    Number.isNaN(month) ||
    Number.isNaN(day) ||
    year <= 0 ||
    month <= 0 ||
    month > 12 ||
    day <= 0 ||
    day > 31
  ) {
    return false;
  }

  const localDate = new Date(year, month - 1, day);
  return (
    localDate.getFullYear() === year &&
    localDate.getMonth() === month - 1 &&
    localDate.getDate() === day
  );
}

export function parseLocalIsoDateOnly(value: string | undefined): Date | undefined {
  if (!value) return undefined;
  const [year, month, day] = value.split('-').map((part) => Number(part));
  if (!isValidLocalDateParts(year, month, day)) return undefined;
  return new Date(year, month - 1, day);
}

export function parseLocalBrDateOnly(value: string | undefined): Date | undefined {
  if (!value) return undefined;
  const masked = FormatDateForm(value);
  if (!/^\d{2}\/\d{2}\/\d{4}$/.test(masked)) return undefined;

  const [dayPart, monthPart, yearPart] = masked.split('/');
  const day = Number(dayPart);
  const month = Number(monthPart);
  const year = Number(yearPart);
  if (!isValidLocalDateParts(year, month, day)) return undefined;

  return new Date(year, month - 1, day);
}

export function toLocalIsoDateOnly(value: Date): string {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, '0');
  const day = String(value.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export function getTodayLocalIsoDateOnly(): string {
  return toLocalIsoDateOnly(new Date());
}

export function normalizeLocalDateOnly(value: string | undefined): string {
  const isoParsed = parseLocalIsoDateOnly(value);
  if (isoParsed) return toLocalIsoDateOnly(isoParsed);

  const brParsed = parseLocalBrDateOnly(value);
  if (brParsed) return toLocalIsoDateOnly(brParsed);

  return getTodayLocalIsoDateOnly();
}
