'use client';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

import { useConfirmacaoBadgeControllerHook } from './hooks/useConfirmacaoBadgeControllerHook';
import ConfirmacaoBadgeInterface from './interfaces/ConfirmacaoBadgeInterface';

export function ConfirmacaoBadge({
  situacao,
  showLabel = true,
  compact = false,
  className,
}: ConfirmacaoBadgeInterface) {
  const { label, Icon, color, bg, size, iconSize } = useConfirmacaoBadgeControllerHook(
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
