"use client";

import { Loader2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";

export interface LoadingDialogProps {
  open: boolean;
  title?: string;
  description?: string;
  className?: string;
}

export function LoadingDialog({
  open,
  title = "Carregando",
  description = "Aguarde um momento...",
  className,
}: LoadingDialogProps) {
  return (
    <Dialog open={open}>
      <DialogContent
        showCloseButton={false}
        className={cn("max-w-sm text-center sm:text-center", className)}
        onInteractOutside={(event) => event.preventDefault()}
        onEscapeKeyDown={(event) => event.preventDefault()}
      >
        <DialogHeader className="items-center gap-4">
          <Loader2
            className="h-10 w-10 animate-spin text-[#FF6B00]"
            aria-hidden
          />
          <div className="space-y-1">
            <DialogTitle>{title}</DialogTitle>
            <DialogDescription>{description}</DialogDescription>
          </div>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
}
