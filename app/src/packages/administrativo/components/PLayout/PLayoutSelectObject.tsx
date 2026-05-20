"use client";

import { useEffect, useMemo } from "react";

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePLayoutReadHook } from "@/packages/administrativo/hooks/PLayout/usePLayoutReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface PLayoutSelectObjectProps {
  /** Valor controlado: `layout_id` como string. */
  value?: string;
  onValueChange?: (layoutId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
}

function layoutLabel(l: { layout_id: number; descricao?: string }) {
  return l.descricao?.trim() || `Layout ${l.layout_id}`;
}

export function PLayoutSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o layout",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum layout disponível",
  optionsOverride,
}: PLayoutSelectObjectProps) {
  const { layouts, isLoading, fetchLayouts } = usePLayoutReadHook();

  useEffect(() => {
    void fetchLayouts();
  }, [fetchLayouts]);

  const options = useMemo(() => {
    if (optionsOverride && optionsOverride.length > 0) {
      return optionsOverride;
    }
    return layouts.map((l) => ({ value: String(l.layout_id), label: layoutLabel(l) }));
  }, [optionsOverride, layouts]);

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
          <SelectItem value="__playout_loading" disabled>
            Carregando layouts...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__playout_empty" disabled>
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
