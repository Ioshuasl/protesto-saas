"use client";

import type { Control } from "react-hook-form";
import { Checkbox } from "@/components/ui/checkbox";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { emolumentoItemOptions } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailSelectOptions";
import type { PTituloDetailsFormValues, PTituloSelectOptionsByField } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import {
  formatPTituloFieldLabel,
  mergeTituloSelectOptions,
  sanitizePTituloPositiveNumber,
} from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";

interface PTituloFeesSectionProps {
  control: Control<PTituloDetailsFormValues>;
  selectOptionsByField?: PTituloSelectOptionsByField;
}

export function PTituloFeesSection({ control, selectOptionsByField }: PTituloFeesSectionProps) {
  return (
    <div className="space-y-3 rounded-md border p-4">
      <h3 className="text-sm font-semibold text-foreground">Emolumentos e custas</h3>

      <div className="grid gap-3 md:grid-cols-3">
        <FormField
          control={control}
          name="tabela_emolumento_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tabela de emolumento</FormLabel>
              <FormControl>
                <Input
                  type="text"
                  inputMode="numeric"
                  {...field}
                  value={field.value ?? ""}
                  onChange={(event) =>
                    field.onChange(sanitizePTituloPositiveNumber(event.target.value, false))
                  }
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="emolumento_item_id"
          render={({ field }) => {
            const merged = mergeTituloSelectOptions(
              "emolumento_item_id",
              emolumentoItemOptions,
              selectOptionsByField,
            );
            const selected = merged.find((option) => option.value === (field.value || ""));
            return (
              <FormItem>
                <FormLabel>Item de emolumento</FormLabel>
                <Select value={field.value || ""} onValueChange={field.onChange}>
                  <FormControl>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Selecione o item de emolumento">{selected?.label}</SelectValue>
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {merged.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            );
          }}
        />
        <FormField
          control={control}
          name="valor_emolumento"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_emolumento")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_judiciaria"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_judiciaria")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_intimacao"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_intimacao")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_desconto"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_desconto")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_edital"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_edital")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_juros"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_juros")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_correios"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_correios")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_cancel"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_cancel")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_averb"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_averb")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_taxa_fundesp"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_taxa_fundesp")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_iss"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_iss")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={control}
          name="valor_total_custas"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{formatPTituloFieldLabel("valor_total_custas")}</FormLabel>
              <FormControl>
                <div className="relative">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">
                    R$
                  </span>
                  <Input
                    type="text"
                    inputMode="decimal"
                    className="pl-10"
                    {...field}
                    value={field.value ?? ""}
                    onChange={(event) =>
                      field.onChange(sanitizePTituloPositiveNumber(event.target.value, true))
                    }
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
      </div>

      <div className="grid gap-3 md:grid-cols-3">
        <FormField
          control={control}
          name="servico_gratuito"
          render={({ field }) => {
            const checked = field.value === "S" || field.value === "true" || field.value === "1";
            return (
              <FormItem>
                <FormLabel>Serviço gratuito</FormLabel>
                <FormControl>
                  <div className="flex h-10 items-center gap-2 rounded-md border px-3">
                    <Checkbox checked={checked} onCheckedChange={(value) => field.onChange(value ? "S" : "N")} />
                    <span className="text-sm text-muted-foreground">{checked ? "Sim" : "Não"}</span>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            );
          }}
        />
        <FormField
          control={control}
          name="pagamento_posterior"
          render={({ field }) => {
            const checked = field.value === "S" || field.value === "true" || field.value === "1";
            return (
              <FormItem>
                <FormLabel>Pagamento posterior</FormLabel>
                <FormControl>
                  <div className="flex h-10 items-center gap-2 rounded-md border px-3">
                    <Checkbox checked={checked} onCheckedChange={(value) => field.onChange(value ? "S" : "N")} />
                    <span className="text-sm text-muted-foreground">{checked ? "Sim" : "Não"}</span>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            );
          }}
        />
        <FormField
          control={control}
          name="pagamento_diferido"
          render={({ field }) => {
            const checked = field.value === "S" || field.value === "true" || field.value === "1";
            return (
              <FormItem>
                <FormLabel>Pagamento diferido</FormLabel>
                <FormControl>
                  <div className="flex h-10 items-center gap-2 rounded-md border px-3">
                    <Checkbox checked={checked} onCheckedChange={(value) => field.onChange(value ? "S" : "N")} />
                    <span className="text-sm text-muted-foreground">{checked ? "Sim" : "Não"}</span>
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            );
          }}
        />
      </div>
    </div>
  );
}
