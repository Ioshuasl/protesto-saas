// TipoAlienacaoSelectInterface.ts
export default interface TipoAlienacaoSelectInterface {
  field: {
    value?: number;
    onChange: (value: number) => void;
    onBlur?: () => void;
    name?: string;
    ref?: React.Ref<any>;
  };
}
