/**
 * Formata um valor em bytes para string legível (B, KB, MB).
 *
 * @param bytes - Tamanho em bytes (número)
 * @returns String formatada (ex: "512 B", "1.5 KB", "2.3 MB")
 */
export function FormatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
