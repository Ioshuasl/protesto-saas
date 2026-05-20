import { SituacoesAtoValue } from '@/shared/enums/SituacoesAtoEnum';

export default interface SituacoesAtosBadgeInterface {
  situacao?: SituacoesAtoValue | null;
  showLabel?: boolean;
  compact?: boolean;
  className?: string;
}
