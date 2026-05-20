/**
 * Obtém a extensão do arquivo a partir do nome ou caminho.
 *
 * @param filename - Nome do arquivo ou caminho completo
 * @returns A extensão do arquivo (ex: 'png', 'pdf') ou string vazia se não houver
 */
export default function GetFileExtension(filename?: string): string {
  if (!filename) return '';

  // Encontra a posição do último ponto na string
  const lastDotIndex = filename.lastIndexOf('.');

  // Se não houver ponto, retorna vazio.
  // Opcional: verifica se o ponto não é o primeiro caractere (arquivos como .gitignore)
  if (lastDotIndex === -1) {
    return '';
  }

  // Retorna tudo após o último ponto e converte para minúsculas
  return filename.substring(lastDotIndex + 1).toLowerCase();
}
