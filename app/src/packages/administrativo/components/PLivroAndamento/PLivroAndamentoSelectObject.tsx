"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { PLIVRO_ANDAMENTO_LIST_QUERY } from "@/packages/administrativo/data/PLivroAndamento/plivroAndamentoDataConfig";
import { usePLivroAndamentoReadHook } from "@/packages/administrativo/hooks/PLivroAndamento/usePLivroAndamentoReadHook";

export interface PLivroAndamentoSelectObjectProps {
  value?: string;
  onValueChange?: (livroAndamentoId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
}

export function livroLabel(m: {
  livro_andamento_id: number;
  numero_livro?: number;
  sigla?: string;
}) {
  const num = m.numero_livro != null ? String(m.numero_livro) : "-";
  const extra = m.sigla?.trim() ? ` — ${m.sigla}` : "";
  return `Livro ${num}${extra}`;
}

function livroSearchValue(m: {
  livro_andamento_id: number;
  numero_livro?: number;
  sigla?: string;
}) {
  const label = livroLabel(m);
  const parts = [
    m.numero_livro != null ? String(m.numero_livro) : "",
    m.sigla,
    label,
    String(m.livro_andamento_id),
  ];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function PLivroAndamentoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o livro",
  searchPlaceholder = "Buscar livro (número ou sigla)...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum livro em andamento disponível",
}: PLivroAndamentoSelectObjectProps) {
  const { livrosAndamento, isLoading, fetchLivrosAndamento } = usePLivroAndamentoReadHook();

  useEffect(() => {
    void fetchLivrosAndamento(PLIVRO_ANDAMENTO_LIST_QUERY);
  }, [fetchLivrosAndamento]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: livrosAndamento.map((m) => ({
          value: String(m.livro_andamento_id),
          label: livroLabel(m),
          searchValue: livroSearchValue(m),
        })),
        value,
      }),
    [livrosAndamento, value],
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
      loadingMessage="Carregando livros..."
      clearAriaLabel="Limpar livro"
    />
  );
}
