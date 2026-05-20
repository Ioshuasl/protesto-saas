"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { PMotivosCancelamentoInterface } from "@/packages/administrativo/interfaces";
import { PMotivosCancelamentoForm, MotivoCancelamentoFormValues } from "./PMotivosCancelamentoForm";

interface PMotivosCancelamentoDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  motivoCancelamento?: PMotivosCancelamentoInterface | null;
  onSubmit: (data: MotivoCancelamentoFormValues) => void;
  isLoading?: boolean;
}

export function PMotivosCancelamentoDialog({
  open,
  onOpenChange,
  motivoCancelamento,
  onSubmit,
  isLoading,
}: PMotivosCancelamentoDialogProps) {
  const isEditing = !!motivoCancelamento;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[560px]">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Motivo de Cancelamento" : "Novo Motivo de Cancelamento"}
          </DialogTitle>
        </DialogHeader>
        <PMotivosCancelamentoForm
          defaultValues={motivoCancelamento || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
