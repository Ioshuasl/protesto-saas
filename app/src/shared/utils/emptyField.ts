import { EMPTY_FIELD_LABEL } from "@/shared/const";

export function isEmptyFieldValue(value: string | number | null | undefined): boolean {
  if (value === null || value === undefined) {
    return true;
  }
  if (typeof value === "string") {
    return value.trim() === "";
  }
  return false;
}

export function formatEmptyField(value: string | number | null | undefined): string {
  if (isEmptyFieldValue(value)) {
    return EMPTY_FIELD_LABEL;
  }
  return String(value);
}

export function formatEmptyFieldTrimmed(value?: string | null): string {
  const text = value?.trim();
  return text ? text : EMPTY_FIELD_LABEL;
}

export function formatEmptyFieldDate(
  value: Date | string | null | undefined,
  formatter: (date: Date) => string,
): string {
  if (!value) {
    return EMPTY_FIELD_LABEL;
  }
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) {
    return EMPTY_FIELD_LABEL;
  }
  return formatter(date);
}
