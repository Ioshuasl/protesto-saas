/** Rotas em api/packages/v1/administrativo/endpoints/g_emolumento_item_endpoint.py */
export const G_EMOLUMENTO_ITEM_ENDPOINTS = {
  index: (emolumentoId: number, emolumentoPeriodoId: number) =>
    `administrativo/g_emolumento_item/${emolumentoId}/${emolumentoPeriodoId}`,
  listDetails: 'administrativo/g_emolumento_item/list-details',
  show: (id: number) => `administrativo/g_emolumento_item/${id}`,
  create: 'administrativo/g_emolumento_item/',
  update: (id: number) => `administrativo/g_emolumento_item/${id}`,
};
