import { UnmaskCPFCNPJForm } from './UnmaskCPFCNPJForm';

export function isCpf(value: string): boolean {
  return UnmaskCPFCNPJForm(value).length <= 11;
}

export function FormatCPFCNPJForm(value: string = ''): string {
  const digits = UnmaskCPFCNPJForm(value);

  // CPF — 11 dígitos
  if (digits.length <= 11) {
    return digits
      .replace(/^(\d{3})(\d)/, '$1.$2')
      .replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3')
      .replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d{1,2})$/, '$1.$2.$3-$4');
  }

  // CNPJ — 14 dígitos
  return digits
    .slice(0, 14)
    .replace(/^(\d{2})(\d)/, '$1.$2')
    .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
    .replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3/$4')
    .replace(/^(\d{2})\.(\d{3})\.(\d{3})\/(\d{4})(\d{1,2})$/, '$1.$2.$3/$4-$5');
}
