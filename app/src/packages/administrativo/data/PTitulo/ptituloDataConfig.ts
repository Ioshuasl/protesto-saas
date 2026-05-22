/** Rotas CRUD em api/packages/v1/administrativo/endpoints/p_titulo_endpoint.py */
export const PTITULO_ENDPOINTS = {
  index: 'administrativo/p_titulo/',
  show: (id: number) => `administrativo/p_titulo/${id}/`,
  selos: (id: number) => `administrativo/p_titulo/${id}/selos`,
  create: 'administrativo/p_titulo/',
  update: (id: number) => `administrativo/p_titulo/${id}/`,
  delete: (id: number) => `administrativo/p_titulo/${id}/`,
};

/**
 * Rotas de fluxo ainda não expostas na API — permanecem em mock até implementação no backend.
 */
export const PTITULO_WORKFLOW_ENDPOINTS = {
  showDevedores: (id: number) => `administrativo/p_titulo/devedores/${id}`,
  /** @deprecated use PTITULO_ENDPOINTS.selos — rota implementada na API */
  selos: (id: number) => PTITULO_ENDPOINTS.selos(id),
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

/** @deprecated use PTITULO_WORKFLOW_ENDPOINTS */
export const PTITULO_FAKE_ENDPOINTS = PTITULO_WORKFLOW_ENDPOINTS;

export function isPTituloWorkflowMockEnabled() {
  return process.env.NEXT_PUBLIC_USE_MOCK_PTITULO_WORKFLOW !== 'false';
}

/** @deprecated use isPTituloWorkflowMockEnabled — CRUD usa API real; só fluxo permanece mockável */
export function isPTituloMockDataEnabled() {
  return isPTituloWorkflowMockEnabled();
}
