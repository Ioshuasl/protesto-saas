"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { PPessoaForm, PessoaFormValues } from "./PPessoaForm";
import { PPessoaInterface } from "@/packages/administrativo/interfaces";

interface PPessoaDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  pessoa?: PPessoaInterface | null;
  onSubmit: (data: PessoaFormValues) => void;
  isLoading?: boolean;
}

export function PPessoaDialog({
  open,
  onOpenChange,
  pessoa,
  onSubmit,
  isLoading,
}: PPessoaDialogProps) {
  const isEditing = !!pessoa;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[900px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Pessoa" : "Nova Pessoa"}
          </DialogTitle>
        </DialogHeader>
        <PPessoaForm
          defaultValues={pessoa || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
