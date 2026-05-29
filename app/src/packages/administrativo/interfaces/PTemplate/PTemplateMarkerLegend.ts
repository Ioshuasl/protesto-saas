export interface PTemplateMarkerLegendItem {
  tag: string;
  color: string;
  label: string;
}

export interface PTemplateMarkerLegend {
  manual: PTemplateMarkerLegendItem;
  automatic: PTemplateMarkerLegendItem;
  variable: PTemplateMarkerLegendItem;
}
