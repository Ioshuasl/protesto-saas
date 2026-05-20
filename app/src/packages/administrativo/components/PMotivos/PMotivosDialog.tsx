"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { PMotivosInterface } from "@/packages/administrativo/interfaces";
import { PMotivosForm, MotivoFormValues } from "./PMotivosForm";

interface PMotivosDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  motivo?: PMotivosInterface | null;
  onSubmit: (data: MotivoFormValues) => void;
  isLoading?: boolean;
}

export function PMotivosDialog({
  open,
  onOpenChange,
  motivo,
  onSubmit,
  isLoading,
}: PMotivosDialogProps) {
  const isEditing = !!motivo;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[520px]">
        <DialogHeader>
          <DialogTitle>{isEditing ? "Editar Motivo de Apontamento" : "Novo Motivo de Apontamento"}</DialogTitle>
        </DialogHeader>
        <PMotivosForm defaultValues={motivo || undefined} onSubmit={onSubmit} isLoading={isLoading} />
      </DialogContent>
    </Dialog>
  );
}
