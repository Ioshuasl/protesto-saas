"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { PEspecieForm, EspecieFormValues } from "./PEspecieForm";
import { PEspecieInterface } from "@/packages/administrativo/interfaces";

interface PEspecieDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  especie?: PEspecieInterface | null;
  onSubmit: (data: EspecieFormValues) => void;
  isLoading?: boolean;
}

export function PEspecieDialog({
  open,
  onOpenChange,
  especie,
  onSubmit,
  isLoading,
}: PEspecieDialogProps) {
  const isEditing = !!especie;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Editar Espécie" : "Nova Espécie"}
          </DialogTitle>
        </DialogHeader>
        <PEspecieForm
          defaultValues={especie || undefined}
          onSubmit={onSubmit}
          isLoading={isLoading}
        />
      </DialogContent>
    </Dialog>
  );
}
