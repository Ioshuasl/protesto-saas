export default interface MarcacaoTipoSelect {
  field: {
    value?: string;
    onChange: (value: string) => void;
    onBlur?: () => void;
    name?: string;
    ref?: React.Ref<any>;
  };
}
