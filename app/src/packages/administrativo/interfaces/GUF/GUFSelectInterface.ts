export default interface GUFSelectInterface {
  field?: {
    value?: number | string;
    onChange?: (value: string | number) => void;
  };
  disable?: boolean;
}
