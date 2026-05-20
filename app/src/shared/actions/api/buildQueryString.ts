/**
 * 🔧 Função genérica responsável por montar uma query string
 * Recebe um objeto qualquer e converte os campos preenchidos em parâmetros de URL.
 * Exemplo: { grupo: 'A', sistema_id: 2 } → "?grupo=A&sistema_id=2"
 */
export function buildQueryString(params: Record<string, any>): string {
  // Retorna uma string no formato ?chave=valor&chave2=valor2 (ou string vazia se não houver parâmetros)
  const query = Object.entries(params || {})
    .filter(([_, value]) => value !== undefined && value !== null && value !== '')
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');

  return query ? `?${query}` : '';
}
