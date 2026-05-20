export const PLIVRO_NATUREZA_FAKE_ENDPOINTS = {
  index: 'administrativo/p_livro_natureza/',
  show: (id: number) => `administrativo/p_livro_natureza/${id}/`,
  create: 'administrativo/p_livro_natureza/',
  update: (id: number) => `administrativo/p_livro_natureza/${id}/`,
  delete: (id: number) => `administrativo/p_livro_natureza/${id}/`,
};

export function usePLivroNaturezaMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PLIVRO_NATUREZA !== 'false';
}
