'use client';

import { AlertCircleIcon } from 'lucide-react';

import { SituacoesAtoValue } from '@/shared/enums/SituacoesAtoEnum';

import { SituacoesAtosBadgeMap } from '../enums/SituacoesAtosBadgeMap';

export const useSituacoesAtosBadgeControllerHook = (
  situacao?: SituacoesAtoValue | null,
  compact?: boolean,
) => {
  const config =
    situacao !== null && situacao !== undefined && SituacoesAtosBadgeMap[situacao]
      ? SituacoesAtosBadgeMap[situacao]
      : {
          label: 'Indefinido',
          icon: AlertCircleIcon,
          color: 'text-gray-600 dark:text-gray-200',
          bg: 'bg-gray-50 dark:bg-gray-800/50',
        };

  const Icon = config.icon;
  const size = compact ? 'h-5 px-2 text-[11px]' : 'h-6 px-2.5 text-xs';
  const iconSize = compact ? 'h-3.5 w-3.5' : 'h-4 w-4';

  return {
    label: config.label,
    Icon,
    color: config.color,
    bg: config.bg,
    size,
    iconSize,
  };
};
