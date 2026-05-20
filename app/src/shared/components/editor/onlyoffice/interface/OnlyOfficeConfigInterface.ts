interface User {
  id?: string;
  name?: string;
}

interface EditorConfig {
  orius_api_endpoint?: string;
  mode?: string;
  lang?: string;
  callbackUrl?: string;
  user?: User;
}

interface Permissions {
  edit?: boolean;
  download?: boolean;
}

interface Document {
  fileType?: string;
  title?: string;
  key?: string;
  permissions?: Permissions;
  url?: string;
}

export default interface OnlyOfficeConfigInterface {
  documentType?: string;
  document?: Document;
  editorConfig?: EditorConfig;
  token?: string;
}
