import type OnlyOfficeConfigInterface from "@/shared/components/editor/onlyoffice/interface/OnlyOfficeConfigInterface";
import type { P_TEMPLATE_ONLYOFFICE_CUSTOMIZATION } from "@/packages/administrativo/constants/pTemplateOnlyOfficeCustomization";

export type PTemplateOnlyOfficeCustomization =
  typeof P_TEMPLATE_ONLYOFFICE_CUSTOMIZATION;

export interface PTemplateOnlyOfficeEditorConfig
  extends NonNullable<OnlyOfficeConfigInterface["editorConfig"]> {
  customization: PTemplateOnlyOfficeCustomization;
}

export interface PTemplateOnlyOfficeConfig extends OnlyOfficeConfigInterface {
  document: NonNullable<OnlyOfficeConfigInterface["document"]>;
  editorConfig: PTemplateOnlyOfficeEditorConfig;
}

