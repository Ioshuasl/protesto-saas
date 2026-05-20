// remove tudo que não for número
const onlyNumbers = (value: string) => value.replace(/\D/g, '');

// ---------- CPF ----------
export function isValidCPF(value: string): boolean {
  const cpf = onlyNumbers(value);

  if (cpf.length !== 11) return false;
  if (/^(\d)\1{10}$/.test(cpf)) return false;

  let sum = 0;
  for (let i = 0; i < 9; i++) sum += Number(cpf[i]) * (10 - i);

  let d1 = (sum * 10) % 11;
  if (d1 === 10) d1 = 0;
  if (d1 !== Number(cpf[9])) return false;

  sum = 0;
  for (let i = 0; i < 10; i++) sum += Number(cpf[i]) * (11 - i);

  let d2 = (sum * 10) % 11;
  if (d2 === 10) d2 = 0;

  return d2 === Number(cpf[10]);
}

// ---------- CNPJ ----------
export function isValidCNPJ(value: string): boolean {
  const cnpj = onlyNumbers(value);

  if (cnpj.length !== 14) return false;
  if (/^(\d)\1{13}$/.test(cnpj)) return false;

  const calcDigit = (base: string, weights: number[]) =>
    base.split('').reduce((sum, num, i) => sum + Number(num) * weights[i], 0) % 11;

  const d1 =
    calcDigit(cnpj.slice(0, 12), [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) < 2
      ? 0
      : 11 - calcDigit(cnpj.slice(0, 12), [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);

  if (d1 !== Number(cnpj[12])) return false;

  const d2 =
    calcDigit(cnpj.slice(0, 13), [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]) < 2
      ? 0
      : 11 - calcDigit(cnpj.slice(0, 13), [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);

  return d2 === Number(cnpj[13]);
}

export function isValidCpfOrCnpj(value: string): boolean {
  const numeric = value.replace(/\D/g, '');

  if (numeric.length === 11) return isValidCPF(numeric);
  if (numeric.length === 14) return isValidCNPJ(numeric);

  return false;
}
