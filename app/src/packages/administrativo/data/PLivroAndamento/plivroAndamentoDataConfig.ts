export const PLIVRO_ANDAMENTO_FAKE_ENDPOINTS = {
  index: 'administrativo/p_livro_andamento/',
  show: (id: number) => `administrativo/p_livro_andamento/${id}/`,
  create: 'administrativo/p_livro_andamento/',
  update: (id: number) => `administrativo/p_livro_andamento/${id}/`,
  delete: (id: number) => `administrativo/p_livro_andamento/${id}/`,
};

export function usePLivroAndamentoMockData() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PLIVRO_ANDAMENTO !== 'false';
}
