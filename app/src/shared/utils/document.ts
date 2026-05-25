import { formatEmptyField, isEmptyFieldValue } from "@/shared/utils/emptyField";

export function formatCpfCnpj(value: string | number | null | undefined): string {
  if (isEmptyFieldValue(value)) {
    return formatEmptyField(value);
  }

  const text = String(value);
  const digits = text.replace(/\D/g, "");

  if (digits.length === 11) {
    return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
  }

  if (digits.length === 14) {
    return digits.replace(
      /(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/,
      "$1.$2.$3/$4-$5",
    );
  }

  return text;
}
