'use client';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

import { useSituacoesAtosBadgeControllerHook } from './hooks/useSituacoesAtosBadgeControllerHook';
import SituacoesAtosBadgeInterface from './interfaces/SituacoesAtosBadgeInterface';

export function SituacoesAtosBadge({
  situacao,
  showLabel = true,
  compact = false,
  className,
}: SituacoesAtosBadgeInterface) {
  const { label, Icon, color, bg, size, iconSize } = useSituacoesAtosBadgeControllerHook(
    situacao,
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
