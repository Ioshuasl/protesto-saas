"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { CalendarIcon } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
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
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { POcorrenciasSelectObject } from "@/packages/administrativo/components/POcorrencias/POcorrenciasSelectObject";
import { usePTituloIntimacaoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloIntimacaoHook";
import type { PTituloIntimacaoInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloIntimacaoInterface";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import {
  pTituloIntimacaoSchema,
  type PTituloIntimacaoFormValues,
} from "@/packages/administrativo/schemas/PTitulo/PTituloIntimacaoSchema";
import { FormatDateTime } from "@/shared/actions/dateTime/FormatDateTime";
import {
  getTodayLocalIsoDateOnly,
  normalizeLocalDateOnly,
  parseLocalIsoDateOnly,
  toLocalIsoDateOnly,
} from "@/shared/actions/dateTime/LocalDateOnly";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";
import { cn } from "@/lib/utils";

export function PTituloIntimacaoButton({ id, onSuccess }: { id: number; onSuccess: (titulo: TituloListItem) => void }) {
  const { intimarTitulo } = usePTituloIntimacaoHook();
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false);

  const form = useForm<PTituloIntimacaoFormValues>({
    resolver: zodResolver(pTituloIntimacaoSchema),
    mode: "onChange",
    defaultValues: {
      ocorrencia_id: 0,
      data_intimacao: getTodayLocalIsoDateOnly(),
    },
  });

  const canSubmit = !isLoading && form.formState.isValid;

  const resetFormState = () => {
    form.reset({
      ocorrencia_id: 0,
      data_intimacao: getTodayLocalIsoDateOnly(),
    });
  };

  const openDialog = () => {
    form.setValue("data_intimacao", getTodayLocalIsoDateOnly(), { shouldValidate: true });
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

  const buildIntimarPayload = (values: PTituloIntimacaoFormValues): PTituloIntimacaoInterface => {
    return {
      ocorrencia_id: Number(values.ocorrencia_id),
      data_intimacao: normalizeLocalDateOnly(String(values.data_intimacao)),
    };
  };

  const handleConfirm = async (values: PTituloIntimacaoFormValues) => {
    const payload = buildIntimarPayload(values);
    setIsLoading(true);
    try {
      const response = await intimarTitulo(id, payload);
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
        variant="default"
        type="button"
        data-skip-global-confirm="true"
        disabled={isLoading}
        className="h-9 rounded-md border bg-[#FF6B00] px-3 text-sm font-medium text-white shadow-none transition-transform duration-200 hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-[#E56000] md:h-10 md:px-4"
        onClick={openDialog}
      >
        Intimar Título
      </Button>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-xl">
          <DialogHeader>
            <DialogTitle>Intimar Título</DialogTitle>
            <DialogDescription>
              Selecione a ocorrência de intimado e a data de intimação para confirmar a ação.
            </DialogDescription>
          </DialogHeader>

          <Form {...form}>
            <form className="grid gap-4 py-1" onSubmit={form.handleSubmit(handleConfirm)}>
              <FormField
                control={form.control}
                name="data_intimacao"
                render={({ field }) => {
                  const selectedDate =
                    typeof field.value === "string" && field.value.length > 0
                      ? parseLocalIsoDateOnly(field.value)
                      : undefined;
                  return (
                    <FormItem>
                      <FormLabel>Data de intimação</FormLabel>
                      <Popover>
                        <FormControl>
                          <PopoverTrigger asChild>
                            <Button
                              type="button"
                              variant="outline"
                              className={cn(
                                "w-full justify-between text-left font-normal",
                                !selectedDate && "text-muted-foreground border-amber-500/40",
                              )}
                            >
                              {selectedDate ? FormatDateTime(selectedDate) : "Selecionar data"}
                              <CalendarIcon className="h-4 w-4 opacity-50" strokeWidth={1.5} />
                            </Button>
                          </PopoverTrigger>
                        </FormControl>
                        <PopoverContent className="w-auto p-0" align="start">
                          <Calendar
                            mode="single"
                            selected={selectedDate}
                            onSelect={(date) =>
                              field.onChange(date ? toLocalIsoDateOnly(date) : getTodayLocalIsoDateOnly())
                            }
                          />
                        </PopoverContent>
                      </Popover>
                      <FormMessage />
                    </FormItem>
                  );
                }}
              />

              <FormField
                control={form.control}
                name="ocorrencia_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Ocorrência de intimado</FormLabel>
                    <FormControl>
                      <POcorrenciasSelectObject
                        value={Number(field.value ?? 0) > 0 ? String(field.value) : ""}
                        onValueChange={(value) => {
                          field.onChange(Number(value));
                        }}
                        triggerClassName={cn(
                          Number(field.value ?? 0) <= 0 && "border-amber-500/40 focus-visible:ring-amber-500/40",
                        )}
                        placeholder="Selecione a ocorrência de intimado"
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
                  Confirmar intimação
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        isOpen={isConfirmDialogOpen}
        title="Intimar Título"
        description="Confirmação obrigatória"
        message="Confirma a intimação deste título com os dados informados?"
        confirmText="Confirmar intimação"
        cancelText="Voltar"
        onConfirm={handleConfirmDialogAction}
        onCancel={closeConfirmDialog}
      />
    </>
  );
}
