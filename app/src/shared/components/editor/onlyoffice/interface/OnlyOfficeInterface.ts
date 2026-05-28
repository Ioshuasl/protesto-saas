import OnlyOfficeConfigInterface from './OnlyOfficeConfigInterface';

export default interface OnlyOfficeInteface {
  id: string;
  config: OnlyOfficeConfigInterface;
  onDocumentError?: (event: unknown) => void;
}
