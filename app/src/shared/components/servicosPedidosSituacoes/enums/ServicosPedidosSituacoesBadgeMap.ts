import { AlertCircleIcon, BadgeCheckIcon, XIcon } from 'lucide-react';

import { ServicosPedidosSituacoesEnum } from '@/shared/enums/ServicosPedidosSituacoesEnum';

export const ServicosPedidosSituacoesBadgeMap = {
  [ServicosPedidosSituacoesEnum.ABERTO]: {
    label: 'Aberto',
    icon: AlertCircleIcon,
    color: 'text-blue-700 dark:text-blue-300',
    bg: 'bg-blue-50 dark:bg-blue-900/20',
  },
  [ServicosPedidosSituacoesEnum.FECHADO]: {
    label: 'Fechado',
    icon: BadgeCheckIcon,
    color: 'text-emerald-700 dark:text-emerald-300',
    bg: 'bg-emerald-50 dark:bg-emerald-900/20',
  },
  [ServicosPedidosSituacoesEnum.CANCELADO]: {
    label: 'Cancelado',
    icon: XIcon,
    color: 'text-red-700 dark:text-red-300',
    bg: 'bg-red-50 dark:bg-red-900/20',
  },
} as const;
