'use client';

import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

import type { PaginationMeta } from './PaginationMeta';

export type PaginationProps = {
  pagination: PaginationMeta;
  onPageChange: (page: number) => void;
  disabled?: boolean;
  className?: string;
  showTotal?: boolean;
};

export function Pagination({
  pagination,
  onPageChange,
  disabled = false,
  className,
  showTotal = true,
}: PaginationProps) {
  const { page, total_pages: totalPages, total, per_page: perPage } = pagination;
  const canGoPrevious = page > 1;
  const canGoNext = totalPages > 0 && page < totalPages;
  const isDisabled = disabled || totalPages === 0;

  const goToPage = (nextPage: number) => {
    if (isDisabled) return;
    const clamped = Math.min(Math.max(nextPage, 1), Math.max(totalPages, 1));
    if (clamped !== page) {
      onPageChange(clamped);
    }
  };

  return (
    <div className={cn('flex shrink-0 flex-wrap items-center justify-between gap-4', className)}>
      <span className="text-muted-foreground text-sm">
        Página {page} de {Math.max(totalPages, 1)}
        {showTotal ? (
          <span className="text-muted-foreground/80">
            {' '}
            · {total} registro{total === 1 ? '' : 's'}
            {perPage > 0 ? ` (${perPage} por página)` : ''}
          </span>
        ) : null}
      </span>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          type="button"
          disabled={isDisabled || !canGoPrevious}
          onClick={() => goToPage(1)}
        >
          Primeira
        </Button>
        <Button
          variant="outline"
          size="sm"
          type="button"
          disabled={isDisabled || !canGoPrevious}
          onClick={() => goToPage(page - 1)}
        >
          <ChevronLeftIcon className="h-4 w-4" />
          Anterior
        </Button>
        <Button
          variant="outline"
          size="sm"
          type="button"
          disabled={isDisabled || !canGoNext}
          onClick={() => goToPage(page + 1)}
        >
          Próxima
          <ChevronRightIcon className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          type="button"
          disabled={isDisabled || !canGoNext}
          onClick={() => goToPage(totalPages)}
        >
          Última
        </Button>
      </div>
    </div>
  );
}
