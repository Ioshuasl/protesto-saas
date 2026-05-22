"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { useGCidadeReadHook } from "@/packages/administrativo/hooks/GCidade/useGCidadeReadHook";
import type GCidadeInterface from "@/packages/administrativo/interfaces/GCidade/GCidadeInterface";

export interface GCidadeSelectObjectProps {
  /** Valor controlado: nome da cidade (`cidade_nome`). */
  value?: string;
  onValueChange?: (cidadeNome: string) => void;
  /** UF usada para filtrar as cidades na API. */
  uf?: string;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  /** Mensagem quando `uf` não estiver definida. */
  ufRequiredMessage?: string;
}

export function cidadeLabel(cidade: { cidade_nome?: string }) {
  return cidade.cidade_nome?.trim().toUpperCase() || "";
}

/** Texto indexado para busca (nome original e label exibido). */
export function cidadeSearchValue(cidade: { cidade_nome?: string }) {
  const nome = String(cidade.cidade_nome ?? "").trim();
  const label = cidadeLabel(cidade);
  return [nome, label].filter(Boolean).join(" ");
}

/**
 * Combobox de cidade (G_CIDADE) alimentado por `useGCidadeReadHook`.
 * Requer `uf` para carregar as opções.
 */
export function GCidadeSelectObject({
  value,
  onValueChange,
  uf,
  placeholder = "Selecione a cidade",
  searchPlaceholder = "Buscar cidade...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma cidade disponível",
  ufRequiredMessage = "Selecione a UF primeiro",
}: GCidadeSelectObjectProps) {
  const [isLoading, setIsLoading] = useState(false);
  const { gCidade, fetchGCidade } = useGCidadeReadHook();
  const lastUfRef = useRef<string | null>(null);

  const normalizedUf = useMemo(
    () =>
      String(uf ?? "")
        .trim()
        .toUpperCase(),
    [uf],
  );

  const isUfMissing = !normalizedUf;

  useEffect(() => {
    if (!normalizedUf) {
      lastUfRef.current = null;
      return;
    }

    if (lastUfRef.current === normalizedUf) {
      return;
    }

    lastUfRef.current = normalizedUf;
    const data: GCidadeInterface = { uf: normalizedUf };
    setIsLoading(true);
    fetchGCidade(data).finally(() => {
      setIsLoading(false);
    });
  }, [normalizedUf, fetchGCidade]);

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: (gCidade ?? []).map((item) => {
          const nome = String(item.cidade_nome ?? "").trim();
          return {
            value: nome,
            label: cidadeLabel(item) || nome,
            searchValue: cidadeSearchValue(item),
          };
        }),
        value,
      }),
    [gCidade, value],
  );

  const resolvedPlaceholder = isUfMissing ? ufRequiredMessage : placeholder;
  const resolvedSearchPlaceholder = isUfMissing ? ufRequiredMessage : searchPlaceholder;
  const resolvedEmptyMessage = isUfMissing ? ufRequiredMessage : emptyMessage;

  return (
    <SearchComboboxSelect
      value={value}
      onValueChange={onValueChange}
      options={options}
      isLoading={isLoading}
      placeholder={resolvedPlaceholder}
      searchPlaceholder={resolvedSearchPlaceholder}
      disabled={disabled || isUfMissing}
      className={className}
      triggerClassName={triggerClassName}
      emptyMessage={resolvedEmptyMessage}
      loadingMessage="Carregando cidades..."
      clearAriaLabel="Limpar cidade"
    />
  );
}
