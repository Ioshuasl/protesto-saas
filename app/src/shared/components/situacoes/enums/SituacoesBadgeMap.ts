import { BadgeCheckIcon, XIcon } from 'lucide-react';

import { SituacoesEnum } from '@/shared/enums/SituacoesEnum';

export const SituacoesBadgeMap = {
  [SituacoesEnum.A]: {
    label: 'Ativo',
    icon: BadgeCheckIcon,
    color: 'text-emerald-700 dark:text-emerald-300',
    bg: 'bg-emerald-50 dark:bg-emerald-900/20',
  },
  [SituacoesEnum.I]: {
    label: 'Inativo',
    icon: XIcon,
    color: 'text-red-700 dark:text-red-300',
    bg: 'bg-red-50 dark:bg-red-900/20',
  },
} as const;
