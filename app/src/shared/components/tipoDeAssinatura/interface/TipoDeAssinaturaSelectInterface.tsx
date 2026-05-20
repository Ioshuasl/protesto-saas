import { TipoDeAssinaturaKey } from '@/shared/enums/TipoDeAssinaturaEnum';

export default interface TipoDeAssinaturaSelectInterface {
  field: {
    value?: TipoDeAssinaturaKey;
    onChange: (value: number) => void;
  };
}
