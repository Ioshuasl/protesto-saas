import type OnlyOfficeConfigInterface from "@/shared/components/editor/onlyoffice/interface/OnlyOfficeConfigInterface";

export interface PTemplateOnlyOfficeConfig extends OnlyOfficeConfigInterface {
  document: NonNullable<OnlyOfficeConfigInterface["document"]>;
  editorConfig: NonNullable<OnlyOfficeConfigInterface["editorConfig"]>;
}

