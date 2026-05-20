export default function GetNameInitials(data?: string): string {
  if (!data) return '';

  // Remove espaços extras no início e no fim e divide em palavras
  const palavras = data.trim().split(/\s+/);

  if (palavras.length === 0) return '';

  if (palavras.length === 1) {
    // Apenas uma palavra → retorna as duas primeiras letras
    return palavras[0].substring(0, 2).toUpperCase();
  }

  // Duas ou mais palavras → retorna a primeira letra das duas primeiras palavras
  return (palavras[0].charAt(0) + palavras[1].charAt(0)).toUpperCase();
}
