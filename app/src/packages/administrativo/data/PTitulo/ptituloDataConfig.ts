export const PTITULO_FAKE_ENDPOINTS = {
  index: 'administrativo/p_titulo/',
  showDevedores: (id: number) => `administrativo/p_titulo/devedores/${id}`,
  show: (id: number) => `administrativo/p_titulo/${id}/`,
  selos: (id: number) => `administrativo/p_titulo/${id}/selos`,
  updateStatus: (id: number) => `administrativo/p_titulo/${id}/status/`,
  voltarIntimacao: (id: number) => `administrativo/p_titulo/voltar_intimacao/${id}`,
  cancelarTitulo: (id: number) => `administrativo/p_titulo/cancelar_titulo/${id}`,
  voltarApontamento: (id: number) => `administrativo/p_titulo/voltar_apontamento/${id}`,
  aceiteEdital: (id: number) => `administrativo/p_titulo/aceite_edital/${id}`,
  desistirTitulo: (id: number) => `administrativo/p_titulo/desistir_titulo/${id}`,
  liquidarTitulo: (id: number) => `administrativo/p_titulo/liquidar_titulo/${id}`,
  protestarTitulo: (id: number) => `administrativo/p_titulo/protestar_titulo/${id}`,
  intimarTitulo: (id: number) => `administrativo/p_titulo/intimar_titulo/${id}`,
  apontarTitulo: (id: number) => `administrativo/p_titulo/apontar_titulo/${id}`,
  proximoNumeroApontamento: () => 'administrativo/p_titulo/proximo_numero_apontamento/',
  voltarProtesto: (id: number) => `administrativo/p_titulo/voltar_protesto/${id}`,
  sustarTitulo: (id: number) => `administrativo/p_titulo/sustar_titulo/${id}`,
  retiradaTitulo: (id: number) => `administrativo/p_titulo/retirada_titulo/${id}`,
};

export function isPTituloMockDataEnabled() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PTITULO !== 'false';
}
