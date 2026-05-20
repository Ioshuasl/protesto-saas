"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePBancoReadHook } from "@/packages/administrativo/hooks/PBanco/usePBancoReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface PBancoSelectObjectProps {
  /** Valor controlado: `banco_id` como string. */
  value?: string;
  onValueChange?: (bancoId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
}

function bancoLabel(b: { banco_id: number; descricao?: string; codigo_banco?: string }) {
  return b.descricao?.trim() || b.codigo_banco?.trim() || `Banco ${b.banco_id}`;
}

export function PBancoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o banco",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum banco disponível",
  optionsOverride,
}: PBancoSelectObjectProps) {
  const { bancos, isLoading, fetchBancos } = usePBancoReadHook();

  useEffect(() => {
    void fetchBancos();
  }, [fetchBancos]);

  const options = useMemo(() => {
    if (optionsOverride && optionsOverride.length > 0) {
      return optionsOverride;
    }
    return bancos.map((b) => ({ value: String(b.banco_id), label: bancoLabel(b) }));
  }, [optionsOverride, bancos]);

  const selectedLabel = useMemo(
    () => options.find((o) => o.value === (value ?? ""))?.label,
    [options, value],
  );

  return (
    <Select
      value={value && value.length > 0 ? value : undefined}
      onValueChange={onValueChange}
      disabled={disabled || (isLoading && !(optionsOverride && optionsOverride.length > 0))}
    >
      <SelectTrigger className={cn("w-full", triggerClassName, className)}>
        <SelectValue placeholder={isLoading && options.length === 0 ? "Carregando..." : placeholder}>
          {selectedLabel}
        </SelectValue>
      </SelectTrigger>
      <SelectContent>
        {isLoading && options.length === 0 ? (
          <SelectItem value="__pbanco_loading" disabled>
            Carregando bancos...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__pbanco_empty" disabled>
            {emptyMessage}
          </SelectItem>
        ) : null}
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
