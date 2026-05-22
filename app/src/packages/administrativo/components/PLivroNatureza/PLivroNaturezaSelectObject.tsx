"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { PLIVRO_NATUREZA_LIST_QUERY } from "@/packages/administrativo/data/PLivroNatureza/plivroNaturezaDataConfig";
import { usePLivroNaturezaReadHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaReadHook";

export interface PLivroNaturezaSelectObjectProps {
  value?: string;
  onValueChange?: (livroNaturezaId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
}

export function naturezaLabel(n: { livro_natureza_id: number; descricao?: string }) {
  return n.descricao?.trim() || `Natureza ${n.livro_natureza_id}`;
}

function naturezaSearchValue(n: { livro_natureza_id: number; descricao?: string }) {
  const label = naturezaLabel(n);
  return [n.descricao, label, String(n.livro_natureza_id)]
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function PLivroNaturezaSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a natureza",
  searchPlaceholder = "Buscar natureza...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma natureza disponível",
}: PLivroNaturezaSelectObjectProps) {
  const { naturezas, isLoading, fetchNaturezas } = usePLivroNaturezaReadHook();

  useEffect(() => {
    void fetchNaturezas(PLIVRO_NATUREZA_LIST_QUERY);
  }, [fetchNaturezas]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: naturezas.map((n) => ({
          value: String(n.livro_natureza_id),
          label: naturezaLabel(n),
          searchValue: naturezaSearchValue(n),
        })),
        value,
      }),
    [naturezas, value],
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
      loadingMessage="Carregando naturezas..."
      clearAriaLabel="Limpar natureza"
    />
  );
}
