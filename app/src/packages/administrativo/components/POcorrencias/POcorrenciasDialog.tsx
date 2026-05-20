"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { POcorrenciasForm, OcorrenciaFormValues } from "./POcorrenciasForm";
import { POcorrenciasInterface } from "@/packages/administrativo/interfaces";

interface POcorrenciasDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  ocorrencia?: POcorrenciasInterface | null;
  onSubmit: (data: OcorrenciaFormValues) => void;
  isLoading?: boolean;
}

export function POcorrenciasDialog({
  open,
  onOpenChange,
  ocorrencia,
  onSubmit,
  isLoading,
}: POcorrenciasDialogProps) {
  const isEditing = !!ocorrencia;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Ocorrência" : "Nova Ocorrência"}
          </DialogTitle>
        </DialogHeader>
        <POcorrenciasForm
          defaultValues={ocorrencia || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
