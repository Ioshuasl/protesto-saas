"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { POCORRENCIA_ANDAMENTO_LIST_QUERY } from "@/packages/administrativo/data/POcorrenciaAndamento/pocorrenciaAndamentoDataConfig";
import {
  ocorrenciaAndamentoLabel,
  ocorrenciaAndamentoSearchValue,
} from "@/packages/administrativo/components/POcorrenciaAndamento/pocorrenciaAndamentoLabelUtils";
import { usePOcorrenciaAndamentoReadHook } from "@/packages/administrativo/hooks/POcorrenciaAndamento/usePOcorrenciaAndamentoReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";

export interface POcorrenciaAndamentoSelectObjectProps {
  /** Valor controlado: `ocorrencia_andamento_id` como string. */
  value?: string;
  onValueChange?: (ocorrenciaAndamentoId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
  selectedLabel?: string;
}

export function POcorrenciaAndamentoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a ocorrência de andamento",
  searchPlaceholder = "Buscar ocorrência (código ou descrição)...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma ocorrência de andamento disponível",
  optionsOverride,
  selectedLabel,
}: POcorrenciaAndamentoSelectObjectProps) {
  const { ocorrenciasAndamento, isLoading, fetchOcorrenciasAndamento } =
    usePOcorrenciaAndamentoReadHook();

  useEffect(() => {
    void fetchOcorrenciasAndamento(POCORRENCIA_ANDAMENTO_LIST_QUERY);
  }, [fetchOcorrenciasAndamento]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: ocorrenciasAndamento.map((item) => ({
          value: String(item.ocorrencia_andamento_id),
          label: ocorrenciaAndamentoLabel(item),
          searchValue: ocorrenciaAndamentoSearchValue(item),
        })),
        optionsOverride,
        value,
        selectedLabel,
      }),
    [ocorrenciasAndamento, optionsOverride, value, selectedLabel],
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
      loadingMessage="Carregando ocorrências..."
      clearAriaLabel="Limpar ocorrência de andamento"
    />
  );
}
