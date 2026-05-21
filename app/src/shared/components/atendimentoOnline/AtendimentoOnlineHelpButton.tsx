'use client';

import { CircleHelpIcon } from 'lucide-react';
import { useState } from 'react';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

import { AtendimentoOnlineDialog } from '@/shared/components/atendimentoOnline/AtendimentoOnlineDialog';

export function AtendimentoOnlineHelpButton() {
  const [dialogOpen, setDialogOpen] = useState(false);

  return (
    <>
      <Button
        type="button"
        variant="outline"
        size="icon"
        className={cn(
          'group bg-background text-foreground fixed bottom-4 right-4 z-50 size-14 shrink-0 rounded-full border-[0.5px] shadow-md',
          'transition-[transform,box-shadow,border-color,background-color,color] duration-200 ease-out',
          'hover:-translate-y-1 hover:scale-105 hover:!bg-primary hover:!text-white hover:!border-primary hover:shadow-lg dark:hover:!bg-primary dark:hover:!text-white',
          'active:translate-y-0 active:scale-[0.97] active:!bg-primary/90 active:!text-white active:!border-primary active:shadow-md dark:active:!bg-primary/90',
          'motion-reduce:transition-none motion-reduce:hover:translate-y-0 motion-reduce:hover:scale-100 motion-reduce:active:scale-100',
        )}
        aria-label="Atendimento online"
        aria-haspopup="dialog"
        aria-expanded={dialogOpen}
        onClick={() => setDialogOpen(true)}
      >
        <CircleHelpIcon
          className={cn(
            'size-8 shrink-0 transition-[transform,color] duration-200 ease-out',
            'group-hover:rotate-6 group-hover:scale-110 group-hover:!text-white',
            'motion-reduce:group-hover:rotate-0 motion-reduce:group-hover:scale-100',
          )}
          aria-hidden
        />
      </Button>

      <AtendimentoOnlineDialog open={dialogOpen} onOpenChange={setDialogOpen} />
    </>
  );
}
