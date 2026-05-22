"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import type { POcorrenciaAndamentoInterface } from "@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface";
import {
  POcorrenciaAndamentoForm,
  type OcorrenciaAndamentoFormValues,
} from "@/packages/administrativo/components/POcorrenciaAndamento/POcorrenciaAndamentoForm";

interface POcorrenciaAndamentoDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  ocorrenciaAndamento?: POcorrenciaAndamentoInterface | null;
  onSubmit: (data: OcorrenciaAndamentoFormValues) => void;
  isLoading?: boolean;
}

export function POcorrenciaAndamentoDialog({
  open,
  onOpenChange,
  ocorrenciaAndamento,
  onSubmit,
  isLoading,
}: POcorrenciaAndamentoDialogProps) {
  const isEditing = !!ocorrenciaAndamento;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[520px]">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar ocorrência de andamento" : "Nova ocorrência de andamento"}
          </DialogTitle>
        </DialogHeader>
        <POcorrenciaAndamentoForm
          defaultValues={ocorrenciaAndamento || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
