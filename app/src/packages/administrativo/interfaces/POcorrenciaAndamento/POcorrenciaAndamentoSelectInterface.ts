export default interface POcorrenciaAndamentoSelectInterface {
  field?: {
    value?: number | string;
    onChange?: (value: string | number) => void;
  };
  disabled?: boolean;
  placeholder?: string;
}
