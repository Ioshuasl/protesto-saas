"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { useGEmolumentoReadHook } from "@/packages/administrativo/hooks/GEmolumento/useGEmolumentoReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface GEmolumentoSelectObjectProps {
  /** Valor controlado: `emolumento_id` como string. */
  value?: string;
  onValueChange?: (emolumentoId: string) => void;
  /** Filtro obrigatório do endpoint: `sistema_id`. */
  sistemaId: number;
  situacao?: string;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
  /** Rótulo quando o valor ainda não está na lista carregada (ex.: show do título). */
  selectedLabel?: string;
}

/** Ex.: descrição do emolumento. */
export function formatEmolumentoSelectLabel(e: {
  emolumento_id?: number;
  descricao?: string;
}) {
  const descricao = e.descricao?.trim();
  if (descricao) return descricao;
  if (e.emolumento_id != null) return `Emolumento ${e.emolumento_id}`;
  return "-";
}

function emolumentoSearchValue(e: {
  emolumento_id?: number;
  descricao?: string;
  tipo?: string;
  modelo_tag?: string;
}) {
  const label = formatEmolumentoSelectLabel(e);
  const parts = [
    e.descricao,
    e.tipo,
    e.modelo_tag,
    label,
    e.emolumento_id != null ? String(e.emolumento_id) : "",
  ];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function GEmolumentoSelectObject({
  value,
  onValueChange,
  sistemaId,
  situacao,
  placeholder = "Selecione o emolumento",
  searchPlaceholder = "Buscar emolumento por descrição...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum emolumento disponível",
  optionsOverride,
  selectedLabel,
}: GEmolumentoSelectObjectProps) {
  const { emolumentos, setEmolumentos, isLoading, fetchEmolumentos } = useGEmolumentoReadHook();
  const hasValidSistemaId = Number.isFinite(sistemaId) && sistemaId > 0;

  useEffect(() => {
    if (!hasValidSistemaId) {
      setEmolumentos([]);
      return;
    }

    void fetchEmolumentos(sistemaId, situacao ? { situacao } : undefined);
  }, [fetchEmolumentos, hasValidSistemaId, setEmolumentos, sistemaId, situacao]);

  const options = useMemo(
    () => {
      const builtOptions = buildSearchComboboxOptions({
        fromFetch: emolumentos.map((e) => ({
          value: String(e.emolumento_id),
          label: formatEmolumentoSelectLabel(e),
          searchValue: emolumentoSearchValue(e),
        })),
        optionsOverride,
        value,
        selectedLabel,
      });

      const normalizedValue = value?.trim();
      if (!normalizedValue) return builtOptions;

      const selectedOption = builtOptions.find((option) => option.value === normalizedValue);
      if (!selectedOption) return builtOptions;

      return [
        selectedOption,
        ...builtOptions.filter((option) => option.value !== normalizedValue),
      ];
    },
    [emolumentos, optionsOverride, value, selectedLabel],
  );

  return (
    <SearchComboboxSelect
      value={value}
      onValueChange={onValueChange}
      options={options}
      isLoading={isLoading}
      placeholder={placeholder}
      searchPlaceholder={searchPlaceholder}
      disabled={disabled || !hasValidSistemaId}
      className={cn("min-w-0", className)}
      triggerClassName={cn("min-w-0", triggerClassName)}
      contentClassName="max-w-[var(--radix-popover-trigger-width)]"
      emptyMessage={emptyMessage}
      loadingMessage="Carregando emolumentos..."
      clearAriaLabel="Limpar emolumento"
    />
  );
}
