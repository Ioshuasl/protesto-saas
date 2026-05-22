"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { usePMotivosReadHook } from "@/packages/administrativo/hooks/PMotivos/usePMotivosReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";

export interface PMotivosSelectObjectProps {
  /** Valor controlado: `motivos_id` como string (identificador do registro em P_MOTIVOS). */
  value?: string;
  onValueChange?: (motivosId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  /** Texto quando a lista vier vazia após o carregamento. */
  emptyMessage?: string;
  /**
   * Quando preenchido, une com a lista do hook (ex.: `selectOptionsByField.motivo_apontamento_id` no formulário de título).
   */
  optionsOverride?: PTituloSelectOption[];
  selectedLabel?: string;
}

export function motivoLabel(m: { descricao?: string; codigo?: string; motivos_id: number }) {
  return m.descricao?.trim() || m.codigo?.trim() || `Motivo ${m.motivos_id}`;
}

function motivoSearchValue(m: { descricao?: string; codigo?: string; motivos_id: number }) {
  const label = motivoLabel(m);
  const parts = [m.descricao, m.codigo, label, String(m.motivos_id)];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

/**
 * Combobox de motivos (P_MOTIVOS) alimentado por `usePMotivosReadHook`.
 * O valor do controle é sempre o id do registro (`motivos_id`, serializado em string).
 */
export function PMotivosSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o motivo",
  searchPlaceholder = "Buscar motivo (código ou descrição)...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum motivo disponível",
  optionsOverride,
  selectedLabel,
}: PMotivosSelectObjectProps) {
  const { motivos, isLoading, fetchMotivos } = usePMotivosReadHook();

  useEffect(() => {
    void fetchMotivos();
  }, [fetchMotivos]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: motivos.map((m) => ({
          value: String(m.motivos_id),
          label: motivoLabel(m),
          searchValue: motivoSearchValue(m),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [motivos, optionsOverride, value, selectedLabel],
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
      loadingMessage="Carregando motivos..."
      clearAriaLabel="Limpar motivo"
    />
  );
}
