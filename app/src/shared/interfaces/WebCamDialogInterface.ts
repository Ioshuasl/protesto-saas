export default interface WebCamDialogInterface {
  isOpen: boolean;
  isLoading: boolean;
  onClose: (item: null, isFormStatus: boolean) => void;
  onSave: (data: string) => void;
}
