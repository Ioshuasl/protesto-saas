export default interface GCidadeSelectInterface {
  field?: {
    value?: number | string;
    onChange?: (value: string | number) => void;
  };
  uf?: string;
  disable?: boolean;
}
