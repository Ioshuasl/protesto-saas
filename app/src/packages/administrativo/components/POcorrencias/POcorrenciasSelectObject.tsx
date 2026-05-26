"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { usePOcorrenciasReadHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface POcorrenciasSelectObjectProps {
  /** Valor controlado: `ocorrencias_id` como string. */
  value?: string;
  onValueChange?: (ocorrenciasId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
  selectedLabel?: string;
}

export function ocorrenciaLabel(o: {
  ocorrencias_id: number;
  descricao?: string;
  tipo?: string;
  codigo?: string;
}) {
  const codigo = o.codigo?.trim();
  const descricao = o.descricao?.trim();
  if (codigo && descricao) return `${codigo} - ${descricao}`;
  return descricao || o.tipo?.trim() || codigo || `Ocorrência ${o.ocorrencias_id}`;
}

function ocorrenciaSearchValue(o: {
  ocorrencias_id: number;
  descricao?: string;
  tipo?: string;
  codigo?: string;
}) {
  const label = ocorrenciaLabel(o);
  const parts = [o.descricao, o.tipo, o.codigo, label, String(o.ocorrencias_id)];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function POcorrenciasSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a ocorrência",
  searchPlaceholder = "Buscar ocorrência...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma ocorrência disponível",
  optionsOverride,
  selectedLabel,
}: POcorrenciasSelectObjectProps) {
  const { ocorrencias, isLoading, fetchOcorrencias } = usePOcorrenciasReadHook();

  useEffect(() => {
    void fetchOcorrencias();
  }, [fetchOcorrencias]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: ocorrencias.map((o) => ({
          value: String(o.ocorrencias_id),
          label: ocorrenciaLabel(o),
          searchValue: ocorrenciaSearchValue(o),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [ocorrencias, optionsOverride, value, selectedLabel],
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
      loadingMessage="Carregando ocorrências..."
      clearAriaLabel="Limpar ocorrência"
    />
  );
}
