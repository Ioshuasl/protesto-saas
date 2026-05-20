export type FileKind = 'image' | 'pdf' | 'sheet' | 'slides' | 'archive' | 'other';

export default interface FileInterface {
  id: string;
  name: string;
  kind?: FileKind | string;
  thumbUrl?: string;
  size?: string;
  activity?: string;
  isNew?: boolean;
}
