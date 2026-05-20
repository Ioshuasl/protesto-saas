'use client';

// Shadcn UI components
import { OctagonAlert } from 'lucide-react';

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

import ConfirmDialogInterface from './interface/ConfirmDialogInterface';

/**
 * Componente de alerta genérico e reutilizável.
 * Baseado no Radix e Shadcn UI, com suporte a título, descrição,
 * mensagem e botões de ação customizáveis.
 */
export default function ConfirmDialog({
  isOpen,
  title,
  description,
  message,
  confirmText = 'Confirmar',
  cancelText = 'Cancelar',
  onConfirm,
  onCancel,
}: ConfirmDialogInterface) {
  return (
    <AlertDialog
      open={isOpen}
      onOpenChange={(open) => {
        if (!open) onCancel();
      }}
    >
      <AlertDialogContent>
        <AlertDialogHeader className="items-center">
          <AlertDialogTitle>
            <div className="bg-destructive/10 mx-auto mb-2 flex h-14 w-14 items-center justify-center rounded-full">
              <OctagonAlert className="text-destructive h-7 w-7" />
            </div>
            {description}: {title}
          </AlertDialogTitle>
          {message && (
            <AlertDialogDescription className="text-center text-[15px]">
              {message}
            </AlertDialogDescription>
          )}
        </AlertDialogHeader>
        <AlertDialogFooter className="mt-2 sm:justify-center">
          <AlertDialogCancel onClick={onCancel} className="cursor-pointer">
            {cancelText}
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirm}
            className={cn('cursor-pointer', buttonVariants({ variant: 'destructive' }))}
          >
            {confirmText}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
