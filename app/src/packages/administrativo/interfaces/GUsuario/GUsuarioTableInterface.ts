import GUsuarioInterface from './GUsuarioInterface';

export default interface GUsuarioTableInterface {
  data?: GUsuarioInterface[];
  onEdit: (item: GUsuarioInterface, isEditingFormStatus: boolean) => void;
  onDelete: (item: GUsuarioInterface, isEditingFormStatus: boolean) => void;
  openModalOnRowClick?: boolean;
}
