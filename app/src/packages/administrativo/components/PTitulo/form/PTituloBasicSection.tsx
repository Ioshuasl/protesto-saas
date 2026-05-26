"use client";

import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { CalendarIcon } from "lucide-react";
import type { Control, FieldPath } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Checkbox } from "@/components/ui/checkbox";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  formatBancoSelectLabel,
  PBancoSelectObject,
} from "@/packages/administrativo/components/PBanco/PBancoSelectObject";
import { POcorrenciasSelectObject } from "@/packages/administrativo/components/POcorrencias/POcorrenciasSelectObject";
import {
  formatEspecieSelectLabel,
  PEspecieSelectObject,
} from "@/packages/administrativo/components/PEspecie/PEspecieSelectObject";
import { cn } from "@/lib/utils";
import { statusImportacaoOptions, tipoEndossoOptions } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailSelectOptions";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import type { PTituloDetailsFormValues, PTituloSelectOptionsByField } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { mergeTituloSelectOptions, parsePTituloIsoDate, sanitizePTituloPositiveNumber } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";
import {
  PTituloFieldGrid,
  PTituloSectionCard,
  ptituloCheckboxRowClassName,
  ptituloDateButtonClassName,
  ptituloFieldLabelClassName,
  ptituloInputClassName,
  ptituloSearchSelectTriggerClassName,
  ptituloSelectTriggerClassName,
} from "./PTituloFormLayout";

interface PTituloBasicSectionProps {
  control: Control<PTituloDetailsFormValues>;
  titulo?: TituloListItem | null;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

type PTituloFieldName = FieldPath<PTituloDetailsFormValues>;
type SelectOption = { value: string; label: string };

function PTituloTextField({
  control,
  name,
  label,
  numeric,
  decimal,
  className,
  inputClassName,
}: {
  control: Control<PTituloDetailsFormValues>;
  name: PTituloFieldName;
  label: string;
  numeric?: boolean;
  decimal?: boolean;
  className?: string;
  inputClassName?: string;
}) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem className={className}>
          <FormLabel className={ptituloFieldLabelClassName}>{label}</FormLabel>
          <FormControl>
            <Input
              type="text"
              inputMode={numeric ? "numeric" : decimal ? "decimal" : undefined}
              className={cn(ptituloInputClassName, inputClassName)}
              {...field}
              value={String(field.value ?? "")}
              onChange={(event) =>
                field.onChange(
                  numeric || decimal
                    ? sanitizePTituloPositiveNumber(event.target.value, Boolean(decimal))
                    : event.target.value,
                )
              }
            />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

function PTituloMoneyField({
  control,
  name,
  label,
  className,
}: {
  control: Control<PTituloDetailsFormValues>;
  name: PTituloFieldName;
  label: string;
  className?: string;
}) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem className={className}>
          <FormLabel className={ptituloFieldLabelClassName}>{label}</FormLabel>
          <FormControl>
            <div className="relative">
              <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                R$
              </span>
              <Input
                type="text"
                inputMode="decimal"
                className={cn(ptituloInputClassName, "pl-9 text-right font-medium")}
                {...field}
                value={String(field.value ?? "")}
                onChange={(event) => field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))}
              />
            </div>
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

function PTituloDateField({
  control,
  name,
  label,
}: {
  control: Control<PTituloDetailsFormValues>;
  name: PTituloFieldName;
  label: string;
}) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => {
        const parsedDate = parsePTituloIsoDate(String(field.value ?? ""));

        return (
          <FormItem className="flex flex-col">
            <FormLabel className={ptituloFieldLabelClassName}>{label}</FormLabel>
            <Popover>
              <FormControl>
                <PopoverTrigger asChild>
                  <Button
                    type="button"
                    variant="outline"
                    className={cn(
                      ptituloDateButtonClassName,
                      "w-full justify-between text-left font-normal",
                      !field.value && "text-muted-foreground",
                    )}
                  >
                    {parsedDate ? format(parsedDate, "dd/MM/yyyy", { locale: ptBR }) : "Selecionar data"}
                    <CalendarIcon className="h-4 w-4 opacity-50" strokeWidth={1.5} />
                  </Button>
                </PopoverTrigger>
              </FormControl>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={parsedDate}
                  onSelect={(date) => field.onChange(date ? format(date, "yyyy-MM-dd") : "")}
                />
              </PopoverContent>
            </Popover>
            <FormMessage />
          </FormItem>
        );
      }}
    />
  );
}

function PTituloSelectField({
  control,
  name,
  label,
  placeholder,
  options,
}: {
  control: Control<PTituloDetailsFormValues>;
  name: PTituloFieldName;
  label: string;
  placeholder: string;
  options: ReadonlyArray<SelectOption>;
}) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel className={ptituloFieldLabelClassName}>{label}</FormLabel>
          <Select value={String(field.value || "")} onValueChange={field.onChange}>
            <FormControl>
              <SelectTrigger className={cn("w-full", ptituloSelectTriggerClassName)}>
                <SelectValue placeholder={placeholder} />
              </SelectTrigger>
            </FormControl>
            <SelectContent>
              {options.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}

function PTituloBooleanField({
  control,
  name,
  label,
}: {
  control: Control<PTituloDetailsFormValues>;
  name: PTituloFieldName;
  label: string;
}) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => {
        const checked = field.value === "S" || field.value === "true" || field.value === "1";
        return (
          <FormItem>
            <FormLabel className={ptituloFieldLabelClassName}>{label}</FormLabel>
            <FormControl>
              <div className={ptituloCheckboxRowClassName}>
                <Checkbox checked={checked} onCheckedChange={(value) => field.onChange(value ? "S" : "N")} />
                <span className="text-sm text-foreground">{checked ? "Sim" : "Não"}</span>
              </div>
            </FormControl>
            <FormMessage />
          </FormItem>
        );
      }}
    />
  );
}

export function PTituloBasicSection({ control, titulo, selectOptionsByField }: PTituloBasicSectionProps) {
  const tipoEndossoMergedOptions = mergeTituloSelectOptions(
    "tipo_endosso",
    tipoEndossoOptions,
    selectOptionsByField,
  );
  const statusImportacaoMergedOptions = mergeTituloSelectOptions(
    "status_importacao",
    statusImportacaoOptions,
    selectOptionsByField,
  );

  return (
    <PTituloSectionCard className="overflow-hidden p-0">
      <div className="border-b border-border/70 px-3 py-2.5 md:px-4">
        <h3 className="text-lg font-semibold tracking-tight text-foreground">Cadastro do título</h3>
      </div>

      <div className="space-y-3 px-3 py-3 md:px-4">
        <PTituloFieldGrid className="lg:grid-cols-4">
          <PTituloTextField control={control} name="numero_titulo" label="Nº do título" numeric />
          <PTituloTextField control={control} name="numero_apontamento" label="Nº do apontamento" numeric />
          <PTituloTextField control={control} name="numero_titulo_banco" label="Título no banco" />
          <PTituloTextField control={control} name="nosso_numero" label="Nosso número" />

          <FormField
            control={control}
            name="especie_id"
            render={({ field }) => (
              <FormItem className="lg:col-span-2">
                <FormLabel className={ptituloFieldLabelClassName}>Espécie do título</FormLabel>
                <FormControl>
                  <PEspecieSelectObject
                    value={field.value}
                    onValueChange={field.onChange}
                    placeholder="Selecione a espécie"
                    optionsOverride={selectOptionsByField?.especie_id}
                    triggerClassName={ptituloSearchSelectTriggerClassName}
                    selectedLabel={
                      titulo?.especie
                        ? formatEspecieSelectLabel(titulo.especie)
                        : titulo?.especie_id != null
                          ? formatEspecieSelectLabel({
                              especie_id: titulo.especie_id,
                              especie: titulo.especie_sigla,
                            })
                          : undefined
                    }
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={control}
            name="ocorrencia_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel className={ptituloFieldLabelClassName}>Ocorrência atual</FormLabel>
                <FormControl>
                  <POcorrenciasSelectObject
                    value={field.value}
                    onValueChange={field.onChange}
                    placeholder="Selecione a ocorrência"
                    optionsOverride={selectOptionsByField?.ocorrencia_id}
                    triggerClassName={ptituloSearchSelectTriggerClassName}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={control}
            name="banco_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel className={ptituloFieldLabelClassName}>Banco apresentante</FormLabel>
                <FormControl>
                  <PBancoSelectObject
                    value={field.value}
                    onValueChange={field.onChange}
                    placeholder="Selecione o banco"
                    optionsOverride={selectOptionsByField?.banco_id}
                    triggerClassName={ptituloSearchSelectTriggerClassName}
                    selectedLabel={
                      titulo?.banco
                        ? formatBancoSelectLabel(titulo.banco)
                        : titulo?.banco_id != null
                          ? formatBancoSelectLabel({ banco_id: titulo.banco_id })
                          : undefined
                    }
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <PTituloSelectField
            control={control}
            name="tipo_endosso"
            label="Endosso"
            placeholder="Selecione o tipo de endosso"
            options={tipoEndossoMergedOptions}
          />
          <PTituloSelectField
            control={control}
            name="status_importacao"
            label="Importação"
            placeholder="Selecione o status de importação"
            options={statusImportacaoMergedOptions}
          />
          <PTituloBooleanField control={control} name="titulo_antigo" label="Título antigo" />
          <PTituloDateField control={control} name="data_emissao_titulo" label="Data de emissão" />
          <PTituloDateField control={control} name="data_vencimento_titulo" label="Data de vencimento" />
          <PTituloDateField control={control} name="data_cadastro" label="Cadastrado em" />
          <PTituloTextField
            control={control}
            name="observacoes"
            label="Observações internas"
            className="lg:col-span-3"
          />
        </PTituloFieldGrid>

        <div className="space-y-2">
          <h4 className="text-sm font-semibold tracking-tight text-foreground">Valores</h4>
          <PTituloFieldGrid className="md:grid-cols-2 lg:grid-cols-2">
            <PTituloMoneyField control={control} name="valor_titulo" label="Valor original" />
            <PTituloMoneyField control={control} name="valor_total" label="Valor atualizado" />
          </PTituloFieldGrid>
        </div>
      </div>
    </PTituloSectionCard>
  );
}
