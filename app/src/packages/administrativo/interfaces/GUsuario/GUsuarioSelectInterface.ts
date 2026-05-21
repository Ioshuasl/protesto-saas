export default interface GTBairroSelectInterface {
  field?: {
    value?: number | string;
    onChange?: (value: string | number) => void;
  };
}
