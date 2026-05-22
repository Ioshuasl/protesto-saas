"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { usePEspecieReadHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";

export interface PEspecieSelectObjectProps {
  /** Valor controlado: `especie_id` como string. */
  value?: string;
  onValueChange?: (especieId: string) => void;
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

/** Ex.: `DMI - DUPLICATA DE VENDA MERCANTIL...` */
export function formatEspecieSelectLabel(e: {
  especie_id?: number;
  descricao?: string;
  especie?: string;
}) {
  const sigla = e.especie?.trim();
  const descricao = e.descricao?.trim();
  if (sigla && descricao) return `${sigla} - ${descricao}`;
  if (descricao) return descricao;
  if (sigla) return sigla;
  if (e.especie_id != null) return `Espécie ${e.especie_id}`;
  return "-";
}

function especieSearchValue(e: {
  especie_id?: number;
  descricao?: string;
  especie?: string;
}) {
  const label = formatEspecieSelectLabel(e);
  const parts = [e.especie, e.descricao, label, e.especie_id != null ? String(e.especie_id) : ""];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function PEspecieSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a espécie",
  searchPlaceholder = "Buscar espécie (sigla ou descrição)...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma espécie disponível",
  optionsOverride,
  selectedLabel,
}: PEspecieSelectObjectProps) {
  const { especies, isLoading, fetchEspecies } = usePEspecieReadHook();

  useEffect(() => {
    void fetchEspecies({ page: 1, per_page: 500, sort: "especie_id.asc" });
  }, [fetchEspecies]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: especies.map((e) => ({
          value: String(e.especie_id),
          label: formatEspecieSelectLabel(e),
          searchValue: especieSearchValue(e),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [especies, optionsOverride, value, selectedLabel],
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
      loadingMessage="Carregando espécies..."
      clearAriaLabel="Limpar espécie"
    />
  );
}
