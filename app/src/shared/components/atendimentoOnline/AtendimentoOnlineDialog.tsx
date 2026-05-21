'use client';

import { ChevronRightIcon, MessageCircleIcon, PhoneIcon } from 'lucide-react';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { cn } from '@/lib/utils';

/** Número exibido: (62) 9 8516-6406 → formato internacional sem símbolos para wa.me */
const WHATSAPP_DISPLAY = '(62) 9 8516-6406';
const WHATSAPP_WA_ME = '5562985166406';

const PHONE_DISPLAY = '(62) 3954-9600';

export type AtendimentoOnlineDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** Classes opcionais no painel do modal */
  contentClassName?: string;
};

const whatsappWebHref = `https://wa.me/${WHATSAPP_WA_ME}`;

export function AtendimentoOnlineDialog({ open, onOpenChange, contentClassName }: AtendimentoOnlineDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={cn('gap-6 sm:max-w-md', contentClassName)}>
        <DialogHeader>
          <DialogTitle>Atendimento online</DialogTitle>
          <DialogDescription>
            Fale com a Orius pelos canais abaixo.
          </DialogDescription>
        </DialogHeader>

        <ul className="grid gap-3" role="list">
          <li className="list-none">
            <a
              href={whatsappWebHref}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`Abrir WhatsApp no número ${WHATSAPP_DISPLAY}`}
              className={cn(
                'bg-muted/40 hover:bg-muted/55 hover:border-primary/25 flex cursor-pointer items-center gap-3 rounded-xl border p-4 shadow-xs transition-colors',
                'focus-visible:ring-ring focus-visible:ring-offset-background outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
              )}
            >
              <span className="bg-background flex size-10 shrink-0 items-center justify-center rounded-full border shadow-xs">
                <MessageCircleIcon className="text-primary size-5" aria-hidden />
              </span>
              <div className="min-w-0 flex-1 space-y-1">
                <p className="font-semibold leading-none">WhatsApp</p>
                <p className="text-muted-foreground text-sm tabular-nums">{WHATSAPP_DISPLAY}</p>
              </div>
              <ChevronRightIcon className="text-muted-foreground size-5 shrink-0" aria-hidden />
            </a>
          </li>

          <li className="bg-muted/40 rounded-xl border p-4">
            <div className="flex items-start gap-3">
              <span className="bg-background mt-0.5 flex size-10 shrink-0 items-center justify-center rounded-full border shadow-xs">
                <PhoneIcon className="text-primary size-5" aria-hidden />
              </span>
              <div className="min-w-0 flex-1 space-y-1">
                <p className="font-semibold leading-none">Telefone fixo</p>
                <p className="text-muted-foreground text-sm tabular-nums">{PHONE_DISPLAY}</p>
              </div>
            </div>
          </li>
        </ul>
      </DialogContent>
    </Dialog>
  );
}
