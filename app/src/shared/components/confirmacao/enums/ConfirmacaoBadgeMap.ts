import { CheckCircleIcon, XCircleIcon } from 'lucide-react';

import { ConfirmacaoValue } from '@/shared/enums/ConfirmacaoEnum';

export const ConfirmacaoBadgeMap: Record<
  ConfirmacaoValue,
  {
    label: string;
    icon: any;
    color: string;
    bg: string;
  }
> = {
  S: {
    label: 'Sim',
    icon: CheckCircleIcon,
    color: 'text-green-700 dark:text-green-300',
    bg: 'bg-green-50 dark:bg-green-900/20',
  },
  N: {
    label: 'Não',
    icon: XCircleIcon,
    color: 'text-red-700 dark:text-red-300',
    bg: 'bg-red-50 dark:bg-red-900/20',
  },
};
