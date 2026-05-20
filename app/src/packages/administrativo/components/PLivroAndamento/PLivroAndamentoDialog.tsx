"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { PLivroAndamentoForm, LivroAndamentoFormValues } from "./PLivroAndamentoForm";
import { PLivroAndamentoInterface } from "@/packages/administrativo/interfaces";

interface PLivroAndamentoDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  livroAndamento?: PLivroAndamentoInterface | null;
  onSubmit: (data: LivroAndamentoFormValues) => void;
  isLoading?: boolean;
}

export function PLivroAndamentoDialog({
  open,
  onOpenChange,
  livroAndamento,
  onSubmit,
  isLoading,
}: PLivroAndamentoDialogProps) {
  const isEditing = !!livroAndamento;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[525px]">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Livro Andamento" : "Novo Livro Andamento"}
          </DialogTitle>
        </DialogHeader>
        <PLivroAndamentoForm
          defaultValues={livroAndamento || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
