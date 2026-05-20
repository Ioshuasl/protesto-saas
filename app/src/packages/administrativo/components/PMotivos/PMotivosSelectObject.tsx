"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePMotivosReadHook } from "@/packages/administrativo/hooks/PMotivos/usePMotivosReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface PMotivosSelectObjectProps {
  /** Valor controlado: `motivos_id` como string (identificador do registro em P_MOTIVOS). */
  value?: string;
  onValueChange?: (motivosId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  /** Texto quando a lista vier vazia após o carregamento. */
  emptyMessage?: string;
  /**
   * Quando preenchido, substitui a lista vinda do hook (ex.: `selectOptionsByField.motivo_apontamento_id` no formulário de título).
   */
  optionsOverride?: PTituloSelectOption[];
}

function motivoLabel(m: { descricao?: string; codigo?: string; motivos_id: number }) {
  return m.descricao?.trim() || m.codigo?.trim() || `Motivo ${m.motivos_id}`;
}

/**
 * Select de motivos (P_MOTIVOS) alimentado por `usePMotivosReadHook`.
 * O valor do controle é sempre o id do registro (`motivos_id`, serializado em string);
 * na interface mostra-se a descrição (com fallback para código).
 */
export function PMotivosSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o motivo",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum motivo disponível",
  optionsOverride,
}: PMotivosSelectObjectProps) {
  const { motivos, isLoading, fetchMotivos } = usePMotivosReadHook();

  useEffect(() => {
    void fetchMotivos();
  }, [fetchMotivos]);

  const options = useMemo(() => {
    if (optionsOverride && optionsOverride.length > 0) {
      return optionsOverride;
    }
    return motivos.map((m) => ({ value: String(m.motivos_id), label: motivoLabel(m) }));
  }, [optionsOverride, motivos]);

  return (
    <Select
      value={value && value.length > 0 ? value : undefined}
      onValueChange={onValueChange}
      disabled={disabled || (isLoading && !(optionsOverride && optionsOverride.length > 0))}
    >
      <SelectTrigger className={cn("w-full", triggerClassName, className)}>
        <SelectValue placeholder={isLoading && options.length === 0 ? "Carregando..." : placeholder} />
      </SelectTrigger>
      <SelectContent>
        {isLoading && options.length === 0 ? (
          <SelectItem value="__pmotivos_loading" disabled>
            Carregando motivos...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__pmotivos_empty" disabled>
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
