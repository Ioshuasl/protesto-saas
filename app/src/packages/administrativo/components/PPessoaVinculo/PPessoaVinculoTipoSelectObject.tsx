"use client";

import { useMemo } from "react";
import {
  SearchComboboxSelect,
  type SearchComboboxOption,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import {
  PPessoaVinculoTipoEnum,
  PPessoaVinculoTipoLabels,
  PPessoaVinculoTipoValues,
  formatPPessoaVinculoTipoLabel,
  normalizePPessoaVinculoTipo,
  pessoaVinculoTipoSearchValue,
  type PPessoaVinculoTipo,
} from "@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoTipoEnum";

export interface PPessoaVinculoTipoSelectObjectProps {
  /** Valor controlado: `APRESENTANTE`, `CEDENTE`, `CREDOR` ou `DEVEDOR`. */
  value?: string;
  onValueChange?: (tipo: PPessoaVinculoTipo | "") => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  /** Subconjunto de tipos exibidos (padrão: todos). */
  allowedTypes?: PPessoaVinculoTipo[];
  clearable?: boolean;
}

function buildTipoOptions(allowedTypes?: PPessoaVinculoTipo[]): SearchComboboxOption[] {
  const types = allowedTypes?.length ? allowedTypes : PPessoaVinculoTipoValues;
  return types.map((tipo) => ({
    value: tipo,
    label: PPessoaVinculoTipoLabels[tipo],
    searchValue: pessoaVinculoTipoSearchValue(tipo),
  }));
}

/**
 * Combobox de tipo de vínculo (P_PESSOA_VINCULO.TIPO_VINCULO).
 * Opções fixas alinhadas à API: APRESENTANTE, CEDENTE, CREDOR, DEVEDOR.
 */
export function PPessoaVinculoTipoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o tipo de vínculo",
  searchPlaceholder = "Buscar tipo (Apresentante, Devedor...)",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum tipo disponível",
  allowedTypes,
  clearable = true,
}: PPessoaVinculoTipoSelectObjectProps) {
  const normalizedValue = normalizePPessoaVinculoTipo(value) ?? "";

  const options = useMemo(() => {
    const base = buildTipoOptions(allowedTypes);
    if (!normalizedValue || base.some((option) => option.value === normalizedValue)) {
      return base;
    }
    return [
      {
        value: normalizedValue,
        label: formatPPessoaVinculoTipoLabel(normalizedValue),
        searchValue: pessoaVinculoTipoSearchValue(normalizedValue),
      },
      ...base,
    ];
  }, [allowedTypes, normalizedValue]);

  return (
    <SearchComboboxSelect
      value={normalizedValue}
      onValueChange={(next) => {
        if (!next) {
          onValueChange?.("");
          return;
        }
        const tipo = normalizePPessoaVinculoTipo(next);
        onValueChange?.(tipo ?? "");
      }}
      options={options}
      placeholder={placeholder}
      searchPlaceholder={searchPlaceholder}
      disabled={disabled}
      className={className}
      triggerClassName={triggerClassName}
      emptyMessage={emptyMessage}
      clearable={clearable}
      clearAriaLabel="Limpar tipo de vínculo"
    />
  );
}

export { PPessoaVinculoTipoEnum, formatPPessoaVinculoTipoLabel, normalizePPessoaVinculoTipo };
