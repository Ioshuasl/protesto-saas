"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePOcorrenciasReadHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface POcorrenciasSelectObjectProps {
  /** Valor controlado: `ocorrencias_id` como string. */
  value?: string;
  onValueChange?: (ocorrenciasId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
}

function ocorrenciaLabel(o: {
  ocorrencias_id: number;
  descricao?: string;
  tipo?: string;
  codigo?: string;
}) {
  return o.descricao?.trim() || o.tipo?.trim() || o.codigo?.trim() || `Ocorrência ${o.ocorrencias_id}`;
}

export function POcorrenciasSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a ocorrência",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma ocorrência disponível",
  optionsOverride,
}: POcorrenciasSelectObjectProps) {
  const { ocorrencias, isLoading, fetchOcorrencias } = usePOcorrenciasReadHook();

  useEffect(() => {
    void fetchOcorrencias();
  }, [fetchOcorrencias]);

  const options = useMemo(() => {
    if (optionsOverride && optionsOverride.length > 0) {
      return optionsOverride;
    }
    return ocorrencias.map((o) => ({ value: String(o.ocorrencias_id), label: ocorrenciaLabel(o) }));
  }, [optionsOverride, ocorrencias]);

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
          <SelectItem value="__pocorrencias_loading" disabled>
            Carregando ocorrências...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__pocorrencias_empty" disabled>
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
