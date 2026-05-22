import { format } from 'date-fns';

import { FormatDateForm } from '@/shared/actions/dateTime/FormatDateForm';
import { parseLocalBrDateOnly } from '@/shared/actions/dateTime/LocalDateOnly';

const BR_DATE_DISPLAY_REGEX = /^\d{2}\/\d{2}\/\d{4}$/;

export function formatDateToBrDisplay(date: Date | undefined): string {
  if (!date) return '';
  return format(date, 'dd/MM/yyyy');
}

export function maskBrDateInput(raw: string): string {
  return FormatDateForm(raw);
}

export function isCompleteBrDateDisplay(value: string): boolean {
  return BR_DATE_DISPLAY_REGEX.test(value);
}

export function parseBrDisplayToDate(value: string): Date | undefined {
  return parseLocalBrDateOnly(value);
}
