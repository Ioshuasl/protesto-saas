export default class FingerHelper {
  static getNameById(fingerId?: number | null): string {
    switch (fingerId) {
      case 1:
        return 'Polegar direito';
      case 2:
        return 'Indicador direito';
      case 3:
        return 'Médio direito';
      case 4:
        return 'Anelar direito';
      case 5:
        return 'Mínimo direito';
      case 6:
        return 'Polegar esquerdo';
      case 7:
        return 'Indicador esquerdo';
      case 8:
        return 'Médio esquerdo';
      case 9:
        return 'Anelar esquerdo';
      case 10:
        return 'Mínimo esquerdo';
      default:
        return 'Desconhecido';
    }
  }
}
