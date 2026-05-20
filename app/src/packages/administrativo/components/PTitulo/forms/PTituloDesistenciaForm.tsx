"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { CalendarIcon } from "lucide-react";
import { type ReactNode, useEffect, useId, useMemo } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
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
import { Toggle } from "@/components/ui/toggle";
import { PMotivosCancelamentoSelectObject } from "@/packages/administrativo/components/PMotivosCancelamento/PMotivosCancelamentoSelectObject";
import { POcorrenciasSelectObject } from "@/packages/administrativo/components/POcorrencias/POcorrenciasSelectObject";
import { moneyFormatter, tituloServicoGratuitoSn } from "@/packages/administrativo/components/PTitulo/titulo-list-utils";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import {
  pTituloDesistenciaFormSchema,
  type PTituloDesistenciaFormValues,
} from "@/packages/administrativo/schemas/PTitulo/PTituloDesistenciaFormSchema";
import { FormatDateTime } from "@/shared/actions/dateTime/FormatDateTime";
import {
  getTodayLocalIsoDateOnly,
  parseLocalIsoDateOnly,
  toLocalIsoDateOnly,
} from "@/shared/actions/dateTime/LocalDateOnly";
import { cn } from "@/lib/utils";

function tituloDateFieldToIso(value: Date | string | undefined): string | undefined {
  if (value == null) return undefined;
  const d = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(d.getTime())) return undefined;
  return toLocalIsoDateOnly(d);
}

export interface PTituloDesistenciaFormProps {
  titulo?: Partial<TituloListItem> | Partial<PTituloInterface>;
  defaultValues?: Partial<PTituloDesistenciaFormValues>;
  onSubmit?: (values: PTituloDesistenciaFormValues) => void;
  id?: string;
  className?: string;
  children?: ReactNode;
}

export function PTituloDesistenciaForm({
  titulo,
  defaultValues,
  onSubmit,
  id,
  className,
  children,
}: PTituloDesistenciaFormProps) {
  const resolvedDefaults = useMemo((): PTituloDesistenciaFormValues => {
    const dataDesistencia =
      defaultValues?.data_desistencia ??
      tituloDateFieldToIso(titulo?.data_desistencia) ??
      getTodayLocalIsoDateOnly();

    return {
      ocorrencia_id: defaultValues?.ocorrencia_id ?? titulo?.ocorrencia_id ?? 0,
      motivo_cancelamento_id:
        defaultValues?.motivo_cancelamento_id ?? titulo?.motivo_cancelamento ?? 0,
      data_desistencia: dataDesistencia,
      servico_gratuito: defaultValues?.servico_gratuito ?? tituloServicoGratuitoSn(titulo),
    };
  }, [defaultValues, titulo]);

  const form = useForm<PTituloDesistenciaFormValues>({
    resolver: zodResolver(pTituloDesistenciaFormSchema),
    mode: "onChange",
    defaultValues: resolvedDefaults,
  });

  useEffect(() => {
    form.reset(resolvedDefaults);
  }, [form, resolvedDefaults]);

  const valorEmolumentoDisplay = moneyFormatter.format(titulo?.valor_emolumento ?? 0);
  const valorTaxaJudiciariaDisplay = moneyFormatter.format(titulo?.valor_taxa_judiciaria ?? 0);
  const valorIssDisplay = moneyFormatter.format(titulo?.valor_iss ?? 0);
  const valorTaxaIntimacaoDisplay = moneyFormatter.format(titulo?.valor_taxa_intimacao ?? 0);
  const valorTaxaCancelamentoDisplay = moneyFormatter.format(titulo?.valor_taxa_cancel ?? 0);
  const valorTaxaAverbDisplay = moneyFormatter.format(titulo?.valor_taxa_averb ?? 0);

  const servicoGratuitoToggleId = useId();

  return (
    <Form {...form}>
      <form
        id={id}
        className={cn("grid gap-4 py-1", className)}
        onSubmit={
          onSubmit
            ? form.handleSubmit(onSubmit)
            : (e) => {
                e.preventDefault();
              }
        }
      >
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:items-start sm:gap-4">
          <FormField
            control={form.control}
            name="data_desistencia"
            render={({ field }) => {
              const selectedDate =
                typeof field.value === "string" && field.value.length > 0
                  ? parseLocalIsoDateOnly(field.value)
                  : undefined;
              return (
                <FormItem>
                  <FormLabel>Data de desistência</FormLabel>
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
            name="motivo_cancelamento_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Motivo de cancelamento</FormLabel>
                <FormControl>
                  <PMotivosCancelamentoSelectObject
                    value={Number(field.value ?? 0) > 0 ? String(field.value) : ""}
                    onValueChange={(value) => {
                      field.onChange(Number(value));
                    }}
                    triggerClassName={cn(
                      Number(field.value ?? 0) <= 0 && "border-amber-500/40 focus-visible:ring-amber-500/40",
                    )}
                    placeholder="Selecione o motivo de cancelamento"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

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

        <FormField
          control={form.control}
          name="servico_gratuito"
          render={({ field }) => (
            <FormItem className="flex flex-col gap-2 space-y-0">
              <div className="flex min-h-10 flex-col gap-2 rounded-md border border-input bg-transparent px-3 py-2 shadow-xs sm:min-h-[2.25rem] sm:flex-row sm:items-center sm:justify-between">
                <FormLabel
                  htmlFor={servicoGratuitoToggleId}
                  className="!mt-0 flex-1 cursor-pointer text-sm font-normal leading-none"
                >
                  Serviço gratuito
                </FormLabel>
                <FormControl>
                  <Toggle
                    id={servicoGratuitoToggleId}
                    type="button"
                    variant="outline"
                    size="sm"
                    aria-label="Serviço gratuito"
                    pressed={field.value === "S"}
                    onPressedChange={(pressed) => field.onChange(pressed ? "S" : "N")}
                    className="shrink-0 self-end sm:self-auto"
                  />
                </FormControl>
              </div>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4">
          <FormItem>
            <FormLabel>Valor emolumento</FormLabel>
            <FormControl>
              <Input disabled readOnly value={valorEmolumentoDisplay} className="bg-muted/40" />
            </FormControl>
          </FormItem>
          <FormItem>
            <FormLabel>Valor taxa judiciária</FormLabel>
            <FormControl>
              <Input disabled readOnly value={valorTaxaJudiciariaDisplay} className="bg-muted/40" />
            </FormControl>
          </FormItem>
          <FormItem>
            <FormLabel>Valor ISS</FormLabel>
            <FormControl>
              <Input disabled readOnly value={valorIssDisplay} className="bg-muted/40" />
            </FormControl>
          </FormItem>
          <FormItem>
            <FormLabel>Valor taxa intimação</FormLabel>
            <FormControl>
              <Input disabled readOnly value={valorTaxaIntimacaoDisplay} className="bg-muted/40" />
            </FormControl>
          </FormItem>
          <FormItem>
            <FormLabel>Valor taxa cancelamento</FormLabel>
            <FormControl>
              <Input disabled readOnly value={valorTaxaCancelamentoDisplay} className="bg-muted/40" />
            </FormControl>
          </FormItem>
          <FormItem>
            <FormLabel>Valor taxa averbação</FormLabel>
            <FormControl>
              <Input disabled readOnly value={valorTaxaAverbDisplay} className="bg-muted/40" />
            </FormControl>
          </FormItem>
        </div>

        {children}
      </form>
    </Form>
  );
}
