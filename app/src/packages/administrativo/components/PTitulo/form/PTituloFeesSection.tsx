"use client";

import { useEffect, useMemo } from "react";
import type { Control, FieldPath } from "react-hook-form";
import { useFormContext, useWatch } from "react-hook-form";
import { Checkbox } from "@/components/ui/checkbox";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { GEmolumentoSelectObject } from "@/packages/administrativo/components/GEmolumento/GEmolumentoSelectObject";
import type { PTituloDetailsFormValues, PTituloSelectOptionsByField } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { formatPTituloFieldLabel } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";
import { GSistemaEnum } from "@/shared/enums/GSistemaEnum";
import {
  PTituloFieldGrid,
  PTituloSectionCard,
  ptituloCheckboxRowClassName,
  ptituloFieldLabelClassName,
  ptituloSelectTriggerClassName,
} from "./PTituloFormLayout";
import { formatPTituloMoneyValue, parsePTituloMoneyValue } from "./PTituloMoneyUtils";

interface PTituloFeesSectionProps {
  control: Control<PTituloDetailsFormValues>;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

const protestoSistemaId = GSistemaEnum["5"].sistema_id;

const feeCalculationFields = [
  { name: "valor_emolumento", label: formatPTituloFieldLabel("valor_emolumento") },
  { name: "valor_taxa_judiciaria", label: formatPTituloFieldLabel("valor_taxa_judiciaria") },
  { name: "valor_taxa_intimacao", label: formatPTituloFieldLabel("valor_taxa_intimacao") },
  { name: "valor_desconto", label: formatPTituloFieldLabel("valor_desconto") },
  { name: "valor_taxa_edital", label: formatPTituloFieldLabel("valor_taxa_edital") },
  { name: "valor_taxa_juros", label: formatPTituloFieldLabel("valor_taxa_juros") },
  { name: "valor_taxa_correios", label: formatPTituloFieldLabel("valor_taxa_correios") },
  { name: "valor_taxa_cancel", label: formatPTituloFieldLabel("valor_taxa_cancel") },
  { name: "valor_taxa_averb", label: formatPTituloFieldLabel("valor_taxa_averb") },
  { name: "valor_taxa_fundesp", label: formatPTituloFieldLabel("valor_taxa_fundesp") },
  { name: "valor_iss", label: formatPTituloFieldLabel("valor_iss") },
] satisfies ReadonlyArray<{
  name: FieldPath<PTituloDetailsFormValues>;
  label: string;
}>;

const paymentToggleFields = [
  { name: "servico_gratuito", label: "Serviço gratuito" },
  { name: "pagamento_posterior", label: "Pagamento posterior" },
  { name: "pagamento_diferido", label: "Pagamento diferido" },
] satisfies ReadonlyArray<{
  name: FieldPath<PTituloDetailsFormValues>;
  label: string;
}>;

function FeeAmountItem({ label, value }: { label: string; value: unknown }) {
  return (
    <div className="rounded-md border border-border/60 bg-background px-3 py-2">
      <div className="text-xs font-medium leading-none text-muted-foreground">{label}</div>
      <div className="mt-1.5 text-sm font-semibold text-foreground">{formatPTituloMoneyValue(value)}</div>
    </div>
  );
}

function ToggleFormField({
  control,
  name,
  label,
}: {
  control: Control<PTituloDetailsFormValues>;
  name: FieldPath<PTituloDetailsFormValues>;
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
                <Checkbox checked={checked} onCheckedChange={(value) => field.onChange(value === true ? "S" : "N")} />
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

export function PTituloFeesSection({ control, selectOptionsByField }: PTituloFeesSectionProps) {
  const { setValue } = useFormContext<PTituloDetailsFormValues>();
  const feeValues = useWatch({
    control,
    name: feeCalculationFields.map((field) => field.name),
  });
  const totalCustas = useMemo(
    () => feeValues.reduce((total, value) => total + parsePTituloMoneyValue(value), 0),
    [feeValues],
  );

  useEffect(() => {
    setValue("valor_total_custas", totalCustas.toFixed(2), {
      shouldDirty: false,
      shouldTouch: false,
      shouldValidate: false,
    });
  }, [setValue, totalCustas]);

  return (
    <PTituloSectionCard className="overflow-hidden p-0">
      <div className="border-b border-border/70 px-3 py-2.5 md:px-4">
        <h3 className="text-lg font-semibold tracking-tight text-foreground">Emolumentos e Custas</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Configure a base de cálculo e acompanhe os valores gerados pelo sistema.
        </p>
      </div>

      <div className="space-y-3 px-3 py-3 md:px-4">
        <div className="grid gap-x-3 gap-y-3">
          <FormField
            control={control}
            name="tabela_emolumento_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel className={ptituloFieldLabelClassName}>Tabela de emolumento</FormLabel>
                <FormControl>
                  <GEmolumentoSelectObject
                    sistemaId={protestoSistemaId}
                    value={field.value}
                    onValueChange={field.onChange}
                    placeholder="Selecione a tabela de emolumento"
                    optionsOverride={selectOptionsByField?.tabela_emolumento_id}
                    triggerClassName={ptituloSelectTriggerClassName}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <PTituloFieldGrid className="md:grid-cols-3">
            {paymentToggleFields.map((field) => (
              <ToggleFormField key={field.name} control={control} name={field.name} label={field.label} />
            ))}
          </PTituloFieldGrid>
        </div>

        <section className="space-y-2.5 border-t border-border/70 pt-3">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <h4 className="text-sm font-semibold tracking-tight text-foreground">Valores e taxas</h4>
            <div className="flex items-center justify-between gap-4 rounded-md border border-border/70 bg-background px-3 py-2 sm:min-w-64">
              <span className="text-sm font-medium text-muted-foreground">Total das custas</span>
              <span className="text-sm font-semibold text-foreground">{formatPTituloMoneyValue(totalCustas)}</span>
            </div>
          </div>

          <div className="grid gap-2.5 sm:grid-cols-2 lg:grid-cols-4">
            {feeCalculationFields.map((field, index) => (
              <FeeAmountItem key={field.name} label={field.label} value={feeValues[index]} />
            ))}
          </div>

          <div className="border-t border-border/70 pt-3">
            <div className="flex items-center justify-between gap-4">
              <span className="text-sm font-medium text-foreground">Total das taxas calculadas</span>
              <span className="text-sm font-semibold text-foreground">{formatPTituloMoneyValue(totalCustas)}</span>
            </div>
          </div>
        </section>
      </div>
    </PTituloSectionCard>
  );
}
