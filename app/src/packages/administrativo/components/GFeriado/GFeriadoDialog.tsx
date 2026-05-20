"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { GFeriadoForm, FeriadoFormValues } from "./GFeriadoForm";
import { GFeriadoInterface } from "@/packages/administrativo/interfaces";

interface GFeriadoDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  feriado?: GFeriadoInterface | null;
  onSubmit: (data: FeriadoFormValues & { dia: number; mes: number; ano: number }) => void;
  isLoading?: boolean;
}

export function GFeriadoDialog({
  open,
  onOpenChange,
  feriado,
  onSubmit,
  isLoading,
}: GFeriadoDialogProps) {
  const isEditing = !!feriado;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Feriado" : "Novo Feriado"}
          </DialogTitle>
        </DialogHeader>
        <GFeriadoForm
          defaultValues={feriado || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
