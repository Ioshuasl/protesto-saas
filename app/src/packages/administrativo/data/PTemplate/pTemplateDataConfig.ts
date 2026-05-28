/** Rotas em api/packages/v1/administrativo/endpoints/p_template_endpoint.py */
export const PTEMPLATE_ENDPOINTS = {
  index: 'administrativo/p_template/',
  show: (id: number) => `administrativo/p_template/${id}`,
  create: 'administrativo/p_template/',
  update: (id: number) => `administrativo/p_template/${id}`,
  delete: (id: number) => `administrativo/p_template/${id}`,
  openEditor: (id: number, mode: 'edit' | 'view' = 'edit') =>
    `administrativo/p_template/${id}/texto/editor?mode=${mode}`,
  callback: (id: number) => `administrativo/p_template/${id}/texto/callback`,
};
