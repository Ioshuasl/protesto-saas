"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { normalizeSituacaoKey } from "@/packages/administrativo/components/PLivroNatureza/plivroNaturezaSituacaoUtils";
import { usePMotivosCancelamentoReadHook } from "@/packages/administrativo/hooks/PMotivosCancelamento/usePMotivosCancelamentoReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";

export interface PMotivosCancelamentoSelectObjectProps {
  value?: string;
  onValueChange?: (motivosCancelamentoId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
  selectedLabel?: string;
}

export function motivoCancelamentoLabel(m: {
  descricao?: string;
  motivos_cancelamento_id: number;
}) {
  return m.descricao?.trim() || `Motivo ${m.motivos_cancelamento_id}`;
}

function motivoCancelamentoSearchValue(m: {
  descricao?: string;
  motivos_cancelamento_id: number;
}) {
  const label = motivoCancelamentoLabel(m);
  return [m.descricao, label, String(m.motivos_cancelamento_id)]
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function PMotivosCancelamentoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o motivo de cancelamento",
  searchPlaceholder = "Buscar motivo de cancelamento...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum motivo de cancelamento disponível",
  optionsOverride,
  selectedLabel,
}: PMotivosCancelamentoSelectObjectProps) {
  const { motivosCancelamento, isLoading, fetchMotivosCancelamento } =
    usePMotivosCancelamentoReadHook();

  useEffect(() => {
    void fetchMotivosCancelamento();
  }, [fetchMotivosCancelamento]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: motivosCancelamento
          .filter((m) => normalizeSituacaoKey(m.situacao) === "A")
          .map((m) => ({
            value: String(m.motivos_cancelamento_id),
            label: motivoCancelamentoLabel(m),
            searchValue: motivoCancelamentoSearchValue(m),
          })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [motivosCancelamento, optionsOverride, value, selectedLabel],
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
      clearAriaLabel="Limpar motivo de cancelamento"
    />
  );
}
