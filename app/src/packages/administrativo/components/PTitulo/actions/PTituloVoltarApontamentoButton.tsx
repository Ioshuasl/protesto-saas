"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { POcorrenciasSelectObject } from "@/packages/administrativo/components/POcorrencias/POcorrenciasSelectObject";
import { usePTituloVoltarApontamentoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloVoltarApontamentoHook";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import type { PTituloVoltarApontamentoInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloVoltarApontamentoInterface";
import {
  pTituloVoltarApontamentoSchema,
  type PTituloVoltarApontamentoFormValues,
} from "@/packages/administrativo/schemas/PTitulo/PTituloVoltarApontamentoSchema";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";
import { cn } from "@/lib/utils";

export function PTituloVoltarApontamentoButton({ id, onSuccess }: { id: number; onSuccess: (titulo: TituloListItem) => void }) {
  const { voltarParaApontamento } = usePTituloVoltarApontamentoHook();
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false);

  const form = useForm<PTituloVoltarApontamentoFormValues>({
    resolver: zodResolver(pTituloVoltarApontamentoSchema),
    mode: "onChange",
    defaultValues: {
      ocorrencia_id: 0,
    },
  });

  const canSubmit = !isLoading && form.formState.isValid;

  const resetFormState = () => {
    form.reset({
      ocorrencia_id: 0,
    });
  };

  const openDialog = () => {
    setIsOpen(true);
  };

  const closeDialog = () => {
    setIsOpen(false);
  };

  const openConfirmDialog = async () => {
    const isValid = await form.trigger();
    if (!isValid) return;
    setIsConfirmDialogOpen(true);
  };

  const closeConfirmDialog = () => {
    setIsConfirmDialogOpen(false);
  };

  const buildVoltarApontamentoPayload = (
    values: PTituloVoltarApontamentoFormValues,
  ): PTituloVoltarApontamentoInterface => {
    return {
      ocorrencia_id: Number(values.ocorrencia_id),
    };
  };

  const handleConfirm = async (values: PTituloVoltarApontamentoFormValues) => {
    const payload = buildVoltarApontamentoPayload(values);
    setIsLoading(true);
    try {
      const response = await voltarParaApontamento(id, payload);
      if (response && typeof response === "object" && "titulo_id" in response) {
        onSuccess(response as TituloListItem);
        closeDialog();
        resetFormState();
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleConfirmDialogAction = () => {
    closeConfirmDialog();
    void form.handleSubmit(handleConfirm)();
  };

  return (
    <>
      <Button
        variant="outline"
        type="button"
        data-skip-global-confirm="true"
        disabled={isLoading}
        className="h-9 rounded-md border bg-muted px-3 text-sm font-medium shadow-none transition-transform duration-200 hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-muted/80 md:h-10 md:px-4"
        onClick={openDialog}
      >
        Voltar para Apontamento
      </Button>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-xl">
          <DialogHeader>
            <DialogTitle>Voltar para Apontamento</DialogTitle>
            <DialogDescription>
              Selecione a ocorrência para confirmar o retorno do título para apontamento.
            </DialogDescription>
          </DialogHeader>

          <Form {...form}>
            <form className="grid gap-4 py-1" onSubmit={form.handleSubmit(handleConfirm)}>
              <FormField
                control={form.control}
                name="ocorrencia_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Ocorrência</FormLabel>
                    <FormControl>
                      <POcorrenciasSelectObject
                        value={Number(field.value ?? 0) > 0 ? String(field.value) : ""}
                        onValueChange={(value) => {
                          field.onChange(Number(value));
                        }}
                        triggerClassName={cn(
                          Number(field.value ?? 0) <= 0 && "border-amber-500/40 focus-visible:ring-amber-500/40",
                        )}
                        placeholder="Selecione a ocorrência"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <DialogFooter>
                <Button type="button" variant="outline" onClick={closeDialog} disabled={isLoading}>
                  Cancelar
                </Button>
                <Button type="button" onClick={openConfirmDialog} disabled={!canSubmit}>
                  Confirmar retorno
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        isOpen={isConfirmDialogOpen}
        title="Voltar para Apontamento"
        description="Confirmação obrigatória"
        message="Confirma o retorno deste título para apontamento com a ocorrência informada?"
        confirmText="Confirmar retorno"
        cancelText="Voltar"
        onConfirm={handleConfirmDialogAction}
        onCancel={closeConfirmDialog}
      />
    </>
  );
}
