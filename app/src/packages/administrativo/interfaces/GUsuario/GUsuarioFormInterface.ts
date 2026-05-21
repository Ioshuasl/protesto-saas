import { GUsuarioFormValues } from '@/packages/administrativo/schemas/GUsuario/GUsuarioSchema';

export interface GUsuarioFormInterface {
  isOpen: boolean;
  data: GUsuarioFormValues | null;
  onClose: (item: null, isFormStatus: boolean) => void;
  onSave: (data: GUsuarioFormValues) => void;
  buttonIsLoading: boolean;
}
