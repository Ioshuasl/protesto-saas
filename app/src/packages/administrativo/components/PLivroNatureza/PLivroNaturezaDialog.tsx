"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { PLivroNaturezaForm, LivroNaturezaFormValues } from "./PLivroNaturezaForm";
import { PLivroNaturezaInterface } from "@/packages/administrativo/interfaces";

interface PLivroNaturezaDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  livroNatureza?: PLivroNaturezaInterface | null;
  onSubmit: (data: LivroNaturezaFormValues) => void;
  isLoading?: boolean;
}

export function PLivroNaturezaDialog({
  open,
  onOpenChange,
  livroNatureza,
  onSubmit,
  isLoading,
}: PLivroNaturezaDialogProps) {
  const isEditing = !!livroNatureza;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Livro Natureza" : "Novo Livro Natureza"}
          </DialogTitle>
        </DialogHeader>
        <PLivroNaturezaForm
          defaultValues={livroNatureza || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
