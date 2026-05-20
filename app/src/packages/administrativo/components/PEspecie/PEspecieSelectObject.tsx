"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePEspecieReadHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface PEspecieSelectObjectProps {
  /** Valor controlado: `especie_id` como string. */
  value?: string;
  onValueChange?: (especieId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
}

function especieLabel(e: { especie_id: number; descricao?: string; especie?: string }) {
  return e.descricao?.trim() || e.especie?.trim() || `Espécie ${e.especie_id}`;
}

export function PEspecieSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a espécie",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma espécie disponível",
  optionsOverride,
}: PEspecieSelectObjectProps) {
  const { especies, isLoading, fetchEspecies } = usePEspecieReadHook();

  useEffect(() => {
    void fetchEspecies();
  }, [fetchEspecies]);

  const options = useMemo(() => {
    if (optionsOverride && optionsOverride.length > 0) {
      return optionsOverride;
    }
    return especies.map((e) => ({ value: String(e.especie_id), label: especieLabel(e) }));
  }, [optionsOverride, especies]);

  const selectedLabel = useMemo(
    () => options.find((o) => o.value === (value ?? ""))?.label,
    [options, value],
  );

  return (
    <Select
      value={value && value.length > 0 ? value : undefined}
      onValueChange={onValueChange}
      disabled={disabled || (isLoading && !(optionsOverride && optionsOverride.length > 0))}
    >
      <SelectTrigger className={cn("w-full", triggerClassName, className)}>
        <SelectValue placeholder={isLoading && options.length === 0 ? "Carregando..." : placeholder}>
          {selectedLabel}
        </SelectValue>
      </SelectTrigger>
      <SelectContent>
        {isLoading && options.length === 0 ? (
          <SelectItem value="__pespecie_loading" disabled>
            Carregando espécies...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__pespecie_empty" disabled>
            {emptyMessage}
          </SelectItem>
        ) : null}
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
