// TipoQualificacaoImovelSelectInterface.ts
export default interface TipoQualificacaoImovelSelectInterface {
  field: {
    value?: number;
    onChange: (value: number) => void;
    onBlur?: () => void;
    name?: string;
    ref?: React.Ref<any>;
  };
}
