"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { useGUfReadHook } from "@/packages/administrativo/hooks/GUF/useGUfReadHook";

export interface GUFSelectObjectProps {
  /** Valor controlado: sigla da UF (ex.: `SP`). */
  value?: string;
  onValueChange?: (sigla: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
}

export function ufLabel(uf: { sigla?: string; nome?: string }) {
  const sigla = uf.sigla?.trim().toUpperCase();
  const nome = uf.nome?.trim();
  if (sigla && nome) return `${sigla} - ${nome}`;
  return sigla || nome || "";
}

/** Texto indexado para busca (sigla, nome e label exibido). */
export function ufSearchValue(uf: { sigla?: string; nome?: string }) {
  const sigla = uf.sigla?.trim() ?? "";
  const nome = uf.nome?.trim() ?? "";
  const label = ufLabel(uf);
  return [label, sigla, nome, `${sigla} ${nome}`].filter(Boolean).join(" ");
}

/**
 * Combobox de UF (G_UF) alimentado por `useGUfReadHook`.
 * O valor do controle é a sigla da UF.
 */
export function GUFSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a UF",
  searchPlaceholder = "Buscar UF...",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma UF disponível",
}: GUFSelectObjectProps) {
  const { gUf, fetchGUf } = useGUfReadHook();
  const didLoadRef = useRef(false);
  const [isLoading, setIsLoading] = useState(false);

  const loadData = useCallback(async () => {
    if (didLoadRef.current) return;
    didLoadRef.current = true;

    try {
      setIsLoading(true);
      await fetchGUf();
    } finally {
      setIsLoading(false);
    }
  }, [fetchGUf]);

  useEffect(() => {
    if (gUf?.length) {
      didLoadRef.current = true;
      return;
    }
    void loadData();
  }, [gUf?.length, loadData]);

  const normalizedValue = value?.trim().toUpperCase() ?? "";

  const options = useMemo(
    () =>
      buildSearchComboboxOptions({
        fromFetch: (gUf ?? [])
          .map((item) => {
            const sigla = item.sigla?.trim().toUpperCase() ?? "";
            if (!sigla) return null;
            return {
              value: sigla,
              label: ufLabel(item) || sigla,
              searchValue: ufSearchValue(item),
            };
          })
          .filter((item): item is NonNullable<typeof item> => item != null),
        value: normalizedValue,
      }),
    [gUf, normalizedValue],
  );

  return (
    <SearchComboboxSelect
      value={normalizedValue}
      onValueChange={(sigla) => onValueChange?.(sigla.trim().toUpperCase())}
      options={options}
      isLoading={isLoading}
      placeholder={placeholder}
      searchPlaceholder={searchPlaceholder}
      disabled={disabled}
      className={className}
      triggerClassName={triggerClassName}
      emptyMessage={emptyMessage}
      loadingMessage="Carregando UFs..."
      clearAriaLabel="Limpar UF"
    />
  );
}
