'use client';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import SituacoesBadgeInterface from '@/shared/components/situacoes/interfaces/SituacoesBadgeInterface';
import { SituacoesEnum } from '@/shared/enums/SituacoesEnum';

import { useSituacoesBadgeControllerHook } from './hooks/useSituacoesBadge';

export function SituacoesBadge({
  situacao,
  showLabel = true,
  compact = false,
  className,
}: SituacoesBadgeInterface) {
  const raw = situacao as string | null | undefined;
  const normalizedSituacao =
    raw && raw in SituacoesEnum
      ? SituacoesEnum[raw as keyof typeof SituacoesEnum]
      : (raw as SituacoesEnum | null | undefined);

  const { label, Icon, color, bg, size, iconSize } = useSituacoesBadgeControllerHook(
    normalizedSituacao,
    compact,
  );

  return (
    <Badge
      className={cn(
        'gap-1.5 rounded-md border border-gray-100 dark:border-gray-700',
        bg,
        size,
        className,
      )}
    >
      <Icon className={cn(iconSize, color)} />
      {showLabel && <span className={cn('font-semibold capitalize', color)}>{label}</span>}
    </Badge>
  );
}
