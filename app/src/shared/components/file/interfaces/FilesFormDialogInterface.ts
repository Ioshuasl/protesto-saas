export default interface FilesFormDialogInterface {
  isOpen: boolean;
  onClose: (isOpen: boolean) => void;
  onSave: (files: File[]) => void;
  title?: string;
  description?: string;
  maxFiles?: number;
  maxSize?: number;
  buttonIsLoading?: boolean;
}
