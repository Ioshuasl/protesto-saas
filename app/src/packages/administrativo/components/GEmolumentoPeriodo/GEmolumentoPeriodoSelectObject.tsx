"use client";

import { useEffect, useMemo } from "react";

import { SearchComboboxSelect } from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { useGEmolumentoPeriodoIndexHook } from "@/packages/administrativo/hooks/GEmolumentoPeriodo/useGEmolumentoPeriodoIndexHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface GEmolumentoPeriodoSelectObjectProps {
  value?: string;
  onValueChange?: (emolumentoPeriodoId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
  selectedLabel?: string;
}

export function formatGEmolumentoPeriodoSelectLabel(p: {
  emolumento_periodo_id?: number;
  descricao?: string;
  situacao?: string;
}) {
  const descricao = p.descricao?.trim();
  const situacao = p.situacao?.trim();

  if (descricao && situacao) return `${descricao} (${situacao})`;
  if (descricao) return descricao;
  if (p.emolumento_periodo_id != null) return `Período ${p.emolumento_periodo_id}`;
  return "-";
}

function gEmolumentoPeriodoSearchValue(p: {
  emolumento_periodo_id?: number;
  descricao?: string;
  situacao?: string;
}) {
  const label = formatGEmolumentoPeriodoSelectLabel(p);
  const parts = [
    p.descricao,
    p.situacao,
    label,
    p.emolumento_periodo_id != null ? String(p.emolumento_periodo_id) : "",
  ];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function GEmolumentoPeriodoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o período de emolumento",
  searchPlaceholder = "Buscar período (ID, descrição ou situação)...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum período de emolumento disponível",
  optionsOverride,
  selectedLabel,
}: GEmolumentoPeriodoSelectObjectProps) {
  const { periodos, isLoading, fetchPeriodos } = useGEmolumentoPeriodoIndexHook();

  useEffect(() => {
    void fetchPeriodos();
  }, [fetchPeriodos]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: periodos.map((periodo) => ({
          value: String(periodo.emolumento_periodo_id),
          label: formatGEmolumentoPeriodoSelectLabel(periodo),
          searchValue: gEmolumentoPeriodoSearchValue(periodo),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [periodos, optionsOverride, value, selectedLabel],
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
      className={cn("min-w-0", className)}
      triggerClassName={cn("min-w-0", triggerClassName)}
      emptyMessage={emptyMessage}
      loadingMessage="Carregando períodos..."
      clearAriaLabel="Limpar período de emolumento"
    />
  );
}
