import { ServicosPedidosSituacoesEnum } from '@/shared/enums/ServicosPedidosSituacoesEnum';

export default interface ServicosPedidosSituacoesBadgeInterface {
  situacao?: ServicosPedidosSituacoesEnum;
  showLabel?: boolean;
  compact?: boolean;
  className?: string;
}
