"use client";

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { GEmolumentoPeriodoForm, type GEmolumentoPeriodoFormValues } from "./GEmolumentoPeriodoForm";
import type { GEmolumentoPeriodoInterface } from "@/packages/administrativo/interfaces/GEmolumentoPeriodo/GEmolumentoPeriodoInterface";

interface GEmolumentoPeriodoDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  periodo?: GEmolumentoPeriodoInterface | null;
  onSubmit: (data: GEmolumentoPeriodoFormValues) => void;
  isLoading?: boolean;
}

export function GEmolumentoPeriodoDialog({
  open,
  onOpenChange,
  periodo,
  onSubmit,
  isLoading,
}: GEmolumentoPeriodoDialogProps) {
  const isEditing = !!periodo;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[520px]">
        <DialogHeader>
          <DialogTitle>{isEditing ? "Editar Periodo de Emolumento" : "Novo Periodo de Emolumento"}</DialogTitle>
        </DialogHeader>
        <GEmolumentoPeriodoForm
          defaultValues={periodo || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
