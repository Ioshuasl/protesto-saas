import FileInterface from './FileInterface';

export default interface FilesIndexInterface {
  title?: string;
  description?: string;
  files: FileInterface[];
  isLoading?: boolean;
  onAdd?: () => void;
  onView?: (file: FileInterface) => void;
  onDownload?: (file: FileInterface) => void;
  onDelete?: (file: FileInterface) => void;
  onShare?: (file: FileInterface) => void;
}
