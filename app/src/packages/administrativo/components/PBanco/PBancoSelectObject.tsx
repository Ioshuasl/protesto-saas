"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { usePBancoReadHook } from "@/packages/administrativo/hooks/PBanco/usePBancoReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface PBancoSelectObjectProps {
  /** Valor controlado: `banco_id` como string. */
  value?: string;
  onValueChange?: (bancoId: string) => void;
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

/** Ex.: `756 - BANCOOB - BANCO COOPERATIVO...` */
export function formatBancoSelectLabel(b: {
  banco_id?: number;
  descricao?: string;
  codigo_banco?: string;
}) {
  const codigo = b.codigo_banco?.trim();
  const descricao = b.descricao?.trim();
  if (codigo && descricao) return `${codigo} - ${descricao}`;
  if (descricao) return descricao;
  if (codigo) return codigo;
  if (b.banco_id != null) return `Banco ${b.banco_id}`;
  return "-";
}

function bancoSearchValue(b: {
  banco_id?: number;
  descricao?: string;
  codigo_banco?: string;
}) {
  const label = formatBancoSelectLabel(b);
  const parts = [
    b.codigo_banco,
    b.descricao,
    label,
    b.banco_id != null ? String(b.banco_id) : "",
  ];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function PBancoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o banco",
  searchPlaceholder = "Buscar banco (código ou descrição)...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum banco disponível",
  optionsOverride,
  selectedLabel,
}: PBancoSelectObjectProps) {
  const { bancos, isLoading, fetchBancos } = usePBancoReadHook();

  useEffect(() => {
    void fetchBancos({ page: 1, per_page: 500, sort: "banco_id.desc" });
  }, [fetchBancos]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: bancos.map((b) => ({
          value: String(b.banco_id),
          label: formatBancoSelectLabel(b),
          searchValue: bancoSearchValue(b),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [bancos, optionsOverride, value, selectedLabel],
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
      loadingMessage="Carregando bancos..."
      clearAriaLabel="Limpar banco"
    />
  );
}
