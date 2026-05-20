"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { CalendarIcon } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
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
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { PMotivosSelectObject } from "@/packages/administrativo/components/PMotivos/PMotivosSelectObject";
import { POcorrenciasSelectObject } from "@/packages/administrativo/components/POcorrencias/POcorrenciasSelectObject";
import { usePTituloApontarHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloApontarHook";
import { usePTituloProximoNumeroApontamentoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloProximoNumeroApontamentoHook";
import type { PTituloApontarInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloApontarInterface";
import { isTituloListItem, type TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import {
  pTituloApontarSchema,
  type PTituloApontarFormValues,
} from "@/packages/administrativo/schemas/PTitulo/PTituloApontarSchema";
import { FormatDateTime } from "@/shared/actions/dateTime/FormatDateTime";
import {
  getTodayLocalIsoDateOnly,
  normalizeLocalDateOnly,
  parseLocalIsoDateOnly,
  toLocalIsoDateOnly,
} from "@/shared/actions/dateTime/LocalDateOnly";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";
import { cn } from "@/lib/utils";

interface PTituloApontarButtonProps {
  id: number;
  numeroApontamento?: number | null;
  onSuccess: (titulo: TituloListItem) => void;
}

export function PTituloApontarButton({ id, numeroApontamento, onSuccess }: PTituloApontarButtonProps) {
  const { apontarTitulo } = usePTituloApontarHook();
  const { proximoNumeroApontamento, isLoading: isLoadingNumero, fetchProximoNumeroApontamento } =
    usePTituloProximoNumeroApontamentoHook();
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isConfirmDialogOpen, setIsConfirmDialogOpen] = useState(false);

  const form = useForm<PTituloApontarFormValues>({
    resolver: zodResolver(pTituloApontarSchema),
    mode: "onChange",
    defaultValues: {
      numero_apontamento: numeroApontamento ?? undefined,
      motivo_apontamento_id: 0,
      ocorrencia_id: 0,
      data_apontamento: getTodayLocalIsoDateOnly(),
    },
  });

  const canSubmit = !isLoading && form.formState.isValid;

  const resetFormState = (numero?: number) => {
    form.reset({
      numero_apontamento: numero,
      motivo_apontamento_id: 0,
      ocorrencia_id: 0,
      data_apontamento: getTodayLocalIsoDateOnly(),
    });
  };

  const openDialog = () => {
    form.setValue("data_apontamento", getTodayLocalIsoDateOnly(), { shouldValidate: true });
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

  const handleConfirmDialogAction = () => {
    closeConfirmDialog();
    void form.handleSubmit(handleConfirm)();
  };

  const buildApontarPayload = (values: PTituloApontarFormValues): PTituloApontarInterface => {
    const parsedDisplayNumber = Number(numeroApontamentoDisplay);
    const numeroApontamento =
      !Number.isNaN(parsedDisplayNumber) && parsedDisplayNumber > 0
        ? parsedDisplayNumber
        : Math.floor(1000 + Math.random() * 900000);

    return {
      numero_apontamento: numeroApontamento,
      motivo_apontamento_id: Number(values.motivo_apontamento_id),
      ocorrencia_id: Number(values.ocorrencia_id),
      data_apontamento: normalizeLocalDateOnly(String(values.data_apontamento)),
    };
  };

  const handleConfirm = async (values: PTituloApontarFormValues) => {
    const payload = buildApontarPayload(values);
    setIsLoading(true);
    try {
      const response = await apontarTitulo(id, payload);
      if (isTituloListItem(response)) {
        onSuccess(response);
        closeDialog();
        resetFormState(response.numero_apontamento ?? undefined);
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!isOpen) return;
    if (typeof numeroApontamento === "number" && numeroApontamento > 0) return;
    if (typeof proximoNumeroApontamento === "number" && proximoNumeroApontamento > 0) return;
    void fetchProximoNumeroApontamento();
  }, [fetchProximoNumeroApontamento, isOpen, numeroApontamento, proximoNumeroApontamento]);

  const numeroApontamentoDisplay = useMemo(() => {
    if (typeof numeroApontamento === "number" && numeroApontamento > 0) {
      return String(numeroApontamento);
    }
    if (typeof proximoNumeroApontamento === "number" && proximoNumeroApontamento > 0) {
      return String(proximoNumeroApontamento);
    }
    return isLoadingNumero ? "Carregando sequência..." : "Não disponível";
  }, [isLoadingNumero, numeroApontamento, proximoNumeroApontamento]);

  useEffect(() => {
    const numero = Number(numeroApontamentoDisplay);
    if (!Number.isNaN(numero) && numero > 0) {
      form.setValue("numero_apontamento", numero, { shouldValidate: true });
    }
  }, [form, numeroApontamentoDisplay]);

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
        Apontar Título
      </Button>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-xl">
          <DialogHeader>
            <DialogTitle>Apontar Título</DialogTitle>
            <DialogDescription>
              Selecione o motivo e a data de apontamento para confirmar a ação.
            </DialogDescription>
          </DialogHeader>

          <Form {...form}>
            <form className="grid gap-4 py-1" onSubmit={form.handleSubmit(handleConfirm)}>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4">
                <FormField
                  control={form.control}
                  name="numero_apontamento"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Número de apontamento</FormLabel>
                      <FormControl>
                        <Input disabled value={numeroApontamentoDisplay} onChange={field.onChange} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="data_apontamento"
                  render={({ field }) => {
                    const selectedDate =
                      typeof field.value === "string" && field.value.length > 0
                        ? parseLocalIsoDateOnly(field.value)
                        : undefined;
                    return (
                      <FormItem>
                        <FormLabel>Data de apontamento</FormLabel>
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
              </div>

              <FormField
                control={form.control}
                name="motivo_apontamento_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Motivo de apontamento</FormLabel>
                    <FormControl>
                      <PMotivosSelectObject
                        value={Number(field.value ?? 0) > 0 ? String(field.value) : ""}
                        onValueChange={(value) => {
                          field.onChange(Number(value));
                        }}
                        triggerClassName={cn(
                          Number(field.value ?? 0) <= 0 && "border-amber-500/40 focus-visible:ring-amber-500/40",
                        )}
                        placeholder="Selecione o motivo"
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
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
                <Button
                  type="button"
                  variant="outline"
                  onClick={closeDialog}
                  disabled={isLoading}
                >
                  Cancelar
                </Button>
                <Button
                  type="button"
                  onClick={openConfirmDialog}
                  disabled={!canSubmit}
                >
                  Confirmar apontamento
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
      <ConfirmDialog
        isOpen={isConfirmDialogOpen}
        title="Apontar Título"
        description="Confirmação obrigatória"
        message="Confirma o apontamento deste título com os dados informados?"
        confirmText="Confirmar apontamento"
        cancelText="Voltar"
        onConfirm={handleConfirmDialogAction}
        onCancel={closeConfirmDialog}
      />
    </>
  );
}
