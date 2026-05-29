/**
 * Customização OnlyOffice exclusiva do fluxo P_TEMPLATE (editor de minutas).
 * @see https://api.onlyoffice.com/docs/docs-api/usage-api/config/editor/customization/
 */
export const P_TEMPLATE_ONLYOFFICE_CUSTOMIZATION = {
  compactHeader: true,
  compactToolbar: true,
  toolbarHideFileName: true,
  hideRightMenu: true,
  hideRulers: true,
  integrationMode: "embed" as const,
  features: {
    tabStyle: { mode: "line" as const },
    tabBackground: { mode: "toolbar" as const },
  },
} as const;
