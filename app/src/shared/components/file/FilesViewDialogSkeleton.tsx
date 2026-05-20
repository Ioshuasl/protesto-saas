'use client';

import { Skeleton } from '@/components/ui/skeleton';

/**
 * Skeleton do conteúdo do FilesViewDialog (área de preview).
 * Usado enquanto imagem ou PDF está carregando.
 */
export default function FilesViewDialogSkeleton() {
  return (
    <div className="flex w-full max-w-full flex-col items-center justify-center gap-4 p-4 sm:p-6">
      <Skeleton className="h-[60vh] w-full max-w-full rounded-lg border sm:max-h-[70vh]" />
    </div>
  );
}
