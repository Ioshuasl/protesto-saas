"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { useGSistemaReadHook } from "@/packages/administrativo/hooks/GSistema/useGSistemaReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface GSistemaSelectObjectProps {
  /** Valor controlado: `sistema_id` como string. */
  value?: string;
  onValueChange?: (sistemaId: string) => void;
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

/** Ex.: `5 - Tabelionato de Protesto` */
export function formatSistemaSelectLabel(s: {
  sistema_id?: number;
  descricao?: string;
  tipo_cartorio?: string;
}) {
  const tipo = s.tipo_cartorio?.trim();
  const descricao = s.descricao?.trim();
  if (tipo && descricao) return `${tipo} - ${descricao}`;
  if (descricao) return descricao;
  if (tipo) return tipo;
  if (s.sistema_id != null) return `Sistema ${s.sistema_id}`;
  return "-";
}

function sistemaSearchValue(s: {
  sistema_id?: number;
  descricao?: string;
  tipo_cartorio?: string;
  versao?: string;
  nome_exe?: string;
}) {
  const label = formatSistemaSelectLabel(s);
  const parts = [
    s.tipo_cartorio,
    s.descricao,
    s.versao,
    s.nome_exe,
    label,
    s.sistema_id != null ? String(s.sistema_id) : "",
  ];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function GSistemaSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o sistema",
  searchPlaceholder = "Buscar sistema (tipo, descrição ou ID)...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum sistema disponível",
  optionsOverride,
  selectedLabel,
}: GSistemaSelectObjectProps) {
  const { sistemas, isLoading, fetchSistemas } = useGSistemaReadHook();

  useEffect(() => {
    void fetchSistemas({ page: 1, per_page: 500, sort: "sistema_id.desc" });
  }, [fetchSistemas]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: sistemas.map((s) => ({
          value: String(s.sistema_id),
          label: formatSistemaSelectLabel(s),
          searchValue: sistemaSearchValue(s),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [sistemas, optionsOverride, value, selectedLabel],
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
      loadingMessage="Carregando sistemas..."
      clearAriaLabel="Limpar sistema"
    />
  );
}
