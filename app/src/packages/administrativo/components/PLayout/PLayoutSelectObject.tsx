"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { usePLayoutReadHook } from "@/packages/administrativo/hooks/PLayout/usePLayoutReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";

export interface PLayoutSelectObjectProps {
  /** Valor controlado: `layout_id` como string. */
  value?: string;
  onValueChange?: (layoutId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
  selectedLabel?: string;
}

export function layoutLabel(l: { layout_id: number; descricao?: string }) {
  return l.descricao?.trim() || `Layout ${l.layout_id}`;
}

function layoutSearchValue(l: { layout_id: number; descricao?: string }) {
  const label = layoutLabel(l);
  return [l.descricao, label, String(l.layout_id)]
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function PLayoutSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o layout",
  searchPlaceholder = "Buscar layout...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum layout disponível",
  optionsOverride,
  selectedLabel,
}: PLayoutSelectObjectProps) {
  const { layouts, isLoading, fetchLayouts } = usePLayoutReadHook();

  useEffect(() => {
    void fetchLayouts();
  }, [fetchLayouts]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: layouts.map((l) => ({
          value: String(l.layout_id),
          label: layoutLabel(l),
          searchValue: layoutSearchValue(l),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [layouts, optionsOverride, value, selectedLabel],
  );

  return (
    <SearchComboboxSelect
      value={value}
      onValueChange={onValueChange}
      options={options}
      isLoading={isLoading}
      placeholder={placeholder}
      searchPlaceholder={searchPlaceholder}
      disabled={disabled}
      className={className}
      triggerClassName={triggerClassName}
      emptyMessage={emptyMessage}
      loadingMessage="Carregando layouts..."
      clearAriaLabel="Limpar layout"
    />
  );
}
