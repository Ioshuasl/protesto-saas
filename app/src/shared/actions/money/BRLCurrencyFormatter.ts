export default class BRLCurrencyFormatter {
  static onlyNumbers(value: string): string {
    if (!value) return '';
    return value.replace(/\D/g, '');
  }

  static format(value?: string | number): string {
    // null, undefined, vazio → zero
    if (value === null || value === undefined || value === '') {
      return 'R$ 0,00';
    }

    let cents: number;

    if (typeof value === 'number') {
      cents = Math.round(value * 100);
    } else {
      const numbers = this.onlyNumbers(value);
      cents = numbers ? Number(numbers) : 0;
    }

    const amount = cents / 100;

    return amount.toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2,
    });
  }

  static toCents(value?: string): number {
    if (!value) return 0;
    const numbers = this.onlyNumbers(value);
    return numbers ? Number(numbers) : 0;
  }
}
