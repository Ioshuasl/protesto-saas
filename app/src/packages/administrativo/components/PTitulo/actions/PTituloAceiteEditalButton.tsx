"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useState } from "react";
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
import { Form } from "@/components/ui/form";
import { PTituloAceiteEditalDevedoresEditor } from "@/packages/administrativo/components/PTitulo/PTituloAceiteEditalDevedoresEditor";
import { usePTituloAceiteEditalHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloAceiteEditalHook";
import { usePTituloShowDevedoresHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloShowDevedoresHook";
import type { PTituloAceiteEditalInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloAceiteEditalInterface";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import {
  pTituloAceiteEditalSchema,
  type PTituloAceiteEditalFormValues,
} from "@/packages/administrativo/schemas/PTitulo/PTituloAceiteEditalSchema";
import {
  getTodayLocalIsoDateOnly,
  normalizeLocalDateOnly,
  toLocalIsoDateOnly,
} from "@/shared/actions/dateTime/LocalDateOnly";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export function PTituloAceiteEditalButton({ id, onSuccess }: { id: number; onSuccess: (titulo: TituloListItem) => void }) {
  const { aceiteEdital } = usePTituloAceiteEditalHook();
  const { devedores, isLoading: isLoadingDevedores, fetchDevedores } = usePTituloShowDevedoresHook();
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false);

  const form = useForm<PTituloAceiteEditalFormValues>({
    resolver: zodResolver(pTituloAceiteEditalSchema),
    mode: "onChange",
    defaultValues: {
      devedores: [],
    },
  });

  const canSubmit = !isLoading && !isLoadingDevedores && form.formState.isValid && devedores.length > 0;

  const resetFormState = () => {
    form.reset({
      devedores: [],
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

  useEffect(() => {
    if (!isOpen) return;
    void (async () => {
      const response = await fetchDevedores(id);
      if (Array.isArray(response)) {
        form.setValue(
          "devedores",
          response.map((devedor) => ({
            pessoa_vinculo_id: devedor.pessoa_vinculo_id,
            devedor_tipo_aceite: devedor.devedor_tipo_aceite ?? "A",
            devedor_data_aceite:
              devedor.devedor_data_aceite instanceof Date
                ? toLocalIsoDateOnly(devedor.devedor_data_aceite)
                : devedor.devedor_data_aceite
                  ? normalizeLocalDateOnly(String(devedor.devedor_data_aceite))
                  : getTodayLocalIsoDateOnly(),
          })),
          { shouldValidate: true },
        );
      }
    })();
  }, [fetchDevedores, form, id, isOpen]);

  const buildAceiteEditalPayload = (values: PTituloAceiteEditalFormValues): PTituloAceiteEditalInterface => {
    return {
      devedores: values.devedores.map((item) => ({
        pessoa_vinculo_id: Number(item.pessoa_vinculo_id),
        devedor_tipo_aceite: item.devedor_tipo_aceite,
        devedor_data_aceite: normalizeLocalDateOnly(item.devedor_data_aceite),
      })),
    };
  };

  const handleConfirm = async (values: PTituloAceiteEditalFormValues) => {
    const payload = buildAceiteEditalPayload(values);
    setIsLoading(true);
    try {
      const response = await aceiteEdital(id, payload);
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
        Aceite/Edital
      </Button>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-6xl">
          <DialogHeader>
            <DialogTitle>Aceite/Edital</DialogTitle>
            <DialogDescription>
              Selecione para cada devedor se o título foi por aceite ou edital, e informe a data correspondente.
            </DialogDescription>
          </DialogHeader>

          <Form {...form}>
            <form className="grid gap-4 py-1" onSubmit={form.handleSubmit(handleConfirm)}>
              <PTituloAceiteEditalDevedoresEditor
                control={form.control}
                devedores={devedores}
                isLoading={isLoadingDevedores}
              />

              <DialogFooter>
                <Button type="button" variant="outline" onClick={closeDialog} disabled={isLoading}>
                  Cancelar
                </Button>
                <Button type="button" onClick={openConfirmDialog} disabled={!canSubmit}>
                  Confirmar aceite/edital
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        isOpen={isConfirmDialogOpen}
        title="Aceite/Edital"
        description="Confirmação obrigatória"
        message="Confirma a atualização de aceite/edital para os devedores informados?"
        confirmText="Confirmar aceite/edital"
        cancelText="Voltar"
        onConfirm={handleConfirmDialogAction}
        onCancel={closeConfirmDialog}
      />
    </>
  );
}
