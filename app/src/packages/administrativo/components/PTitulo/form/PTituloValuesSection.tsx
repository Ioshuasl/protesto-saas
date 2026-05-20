"use client";

import type { Control } from "react-hook-form";
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import type { PTituloDetailsFormValues } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { sanitizePTituloPositiveNumber } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";

interface PTituloValuesSectionProps {
  control: Control<PTituloDetailsFormValues>;
}

export function PTituloValuesSection({ control }: PTituloValuesSectionProps) {
  return (
    <div className="space-y-3 rounded-md border p-4">
      <h3 className="text-sm font-semibold text-foreground">Valores</h3>
      <div className="grid gap-3 md:grid-cols-3">
        <FormField
          control={control}
          name="valor_titulo"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Valor do título</FormLabel>
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
          name="valor_total"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Valor total</FormLabel>
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
    </div>
  );
}
