import { ConfirmacaoValue } from '@/shared/enums/ConfirmacaoEnum';

// ConfirmacaoCheckBoxFormInterface.ts
export default interface ConfirmacaoCheckBoxFormInterface {
  field: {
    value?: ConfirmacaoValue;
    onChange: (value: ConfirmacaoValue) => void;
    onBlur?: () => void;
    name?: string;
    ref?: React.Ref<any>;
  };
  label: string;
}
